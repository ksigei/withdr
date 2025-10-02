from django.contrib import admin
from .models import Wallet, Transaction, BankAccount, Withdrawal


# ---------- INLINES ----------
class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    fields = ("kind", "amount", "note", "created_at")
    readonly_fields = ("created_at",)


class WithdrawalInline(admin.TabularInline):
    model = Withdrawal
    extra = 0
    fields = ("currency", "crypto_amount", "fiat_amount", "fiat_currency", "status", "requested_at", "bank_account")
    readonly_fields = ("requested_at",)


# ---------- MAIN ADMINS ----------
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "currency_display", "balance", "created_at")
    list_filter = ("currency", "created_at")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)
    inlines = [TransactionInline, WithdrawalInline]

    def currency_display(self, obj):
        return obj.get_currency_display()
    currency_display.short_description = "Currency"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "currency_display", "kind", "amount", "created_at")
    list_filter = ("kind", "wallet__currency", "created_at")
    search_fields = ("wallet__user__username", "wallet__user__email", "note")
    ordering = ("-created_at",)

    def currency_display(self, obj):
        return obj.wallet.get_currency_display()
    currency_display.short_description = "Currency"


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "bank_name_display", "account_holder_name", "account_number", "created_at")
    search_fields = ("user__username", "user__email", "bank_name", "account_holder_name", "account_number")
    ordering = ("-created_at",)

    def bank_name_display(self, obj):
        return obj.get_bank_name_display()
    bank_name_display.short_description = "Bank"


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = (
        "wallet", 
        "currency_display", 
        "crypto_amount", 
        "fiat_amount", 
        "fiat_currency", 
        "bank_account", 
        "status", 
        "requested_at"
    )
    list_filter = ("currency", "fiat_currency", "status", "requested_at")
    search_fields = (
        "wallet__user__username", 
        "wallet__user__email", 
        "bank_account__bank_name", 
        "bank_account__account_number"
    )
    ordering = ("-requested_at",)

    def currency_display(self, obj):
        return obj.get_currency_display()
    currency_display.short_description = "Currency"
