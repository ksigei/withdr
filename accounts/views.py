from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

from .models import Wallet, BankAccount, Withdrawal
from .forms import BankAccountForm, WithdrawalForm

@login_required
def dashboard(request):
    wallets = Wallet.objects.filter(user=request.user)
    preferred_bank = request.user.bank_accounts.filter(is_preferred=True).first()
    form = BankAccountForm()
    return render(request, "dashboard.html", {
        "wallets": wallets,
        "preferred_bank": preferred_bank,
        "form": form,
    })

@login_required
def add_bank_account(request):
    if request.method == "POST":
        form = BankAccountForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.user = request.user
            bank.save()
            messages.success(request, "Bank account added successfully.")
            return redirect("accounts:dashboard")
    else:
        form = BankAccountForm()
    return render(request, "bank_form.html", {"form": form})


@login_required
def set_preferred_bank(request):
    if request.method == "POST":
        if "bank_id" in request.POST:  # choosing preferred bank
            bank_id = request.POST.get("bank_id")
            bank = get_object_or_404(BankAccount, id=bank_id, user=request.user)
            request.user.bank_accounts.update(is_preferred=False)
            bank.is_preferred = True
            bank.save()
            messages.success(request, f"{bank.get_bank_name_display()} set as preferred bank.")
        elif "new_bank" in request.POST:  # adding a new bank inline
            form = BankAccountForm(request.POST)
            if form.is_valid():
                bank = form.save(commit=False)
                bank.user = request.user
                bank.is_preferred = True  # new bank becomes preferred
                bank.save()
                request.user.bank_accounts.exclude(id=bank.id).update(is_preferred=False)
                messages.success(request, f"{bank.get_bank_name_display()} added and set as preferred.")
    return redirect("accounts:dashboard")


@login_required
def withdraw(request):
    preferred = request.user.bank_accounts.filter(is_preferred=True).first()
    if not preferred:
        messages.error(request, "You must set a preferred bank before withdrawing.")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = WithdrawalForm(request.POST, user=request.user)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.wallet = form.cleaned_data["wallet"]
            withdrawal.bank_account = preferred
            withdrawal.currency = withdrawal.wallet.currency
            withdrawal.crypto_amount = form.cleaned_data["crypto_amount"]

            # Convert crypto → fiat (dummy rate for now, replace with real API)
            rates = {"BTC": 60000, "ETH": 2000, "USDT": 1, "BNB": 300}
            rate = Decimal(rates.get(withdrawal.currency, 1))
            withdrawal.fiat_amount = withdrawal.crypto_amount * rate
            withdrawal.save()

            # Deduct from wallet
            withdrawal.wallet.debit(withdrawal.crypto_amount, note="Withdrawal")
            messages.success(request, f"Withdrawal of {withdrawal.crypto_amount} {withdrawal.currency} submitted.")
            return redirect("accounts:dashboard")
    else:
        form = WithdrawalForm()

    return render(request, "withdraw_form.html", {"form": form, "preferred_bank": preferred})

@login_required
def banks(request):
    """List all user's bank accounts and allow adding one."""
    banks = request.user.bank_accounts.all()
    return render(request, "banks.html", {"banks": banks})


@login_required
def transactions(request):
    """Show all transactions for the user across wallets."""
    wallets = request.user.wallets.prefetch_related("transactions")
    # flatten transactions
    transactions = []
    for wallet in wallets:
        for tx in wallet.transactions.all():
            transactions.append(tx)
    transactions.sort(key=lambda x: x.created_at, reverse=True)
    return render(request, "transactions.html", {"transactions": transactions})
