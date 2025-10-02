from django import forms
from .models import BankAccount, Withdrawal


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        # fields = ["bank_name", "account_holder_name", "account_number"]
        fields = ["bank_name", "account_number"]  # Removed account_holder_name for simplicity
        widgets = {
            "bank_name": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            # "account_holder_name": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            # "account_number": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
        }


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["wallet", "crypto_amount"]  # fiat is auto-calculated, bank auto-chosen
        widgets = {
            "wallet": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "crypto_amount": forms.NumberInput(attrs={"class": "w-full p-2 border rounded"}),
        }
