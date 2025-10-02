from django.conf import settings
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractUser, BaseUserManager
# ---------------- CUSTOM USER MANAGER ----------------

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# ---------------- CUSTOM USER MODEL ----------------
class CustomUser(AbstractUser):
    username = None  # disable username
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"   # use email to log in
    REQUIRED_FIELDS = []       # no extra required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# ---------------- CRYPTO CHOICES ----------------
CRYPTO_CHOICES = [
    ("BTC", "Bitcoin (BTC)"),
    ("ETH", "Ethereum (ETH)"),
    ("BNB", "Binance Coin (BNB)"),
    ("USDT", "Tether (USDT)"),
    ("USDC", "USD Coin (USDC)"),
    # fiat
    ("USD", "US Dollar (USD)"),
    ("KES", "Kenyan Shilling (KES)"),
    ("EUR", "Euro (EUR)"),
    ("GBP", "British Pound (GBP)"),
    ("JPY", "Japanese Yen (JPY)"),
    ("NGN", "Nigerian Naira (NGN)"),
    ("GHS", "Ghanaian Cedi (GHS)"),
    ("ZAR", "South African Rand (ZAR)"),
    ("UGX", "Ugandan Shilling (UGX)"),
    ("TZS", "Tanzanian Shilling (TZS)"),
    ("RWF", "Rwandan Franc (RWF)"),
    ("XAF", "Central African CFA Franc (XAF)"),
    ("XOF", "West African CFA Franc (XOF)"),
    ("ZMW", "Zambian Kwacha (ZMW)"),
]


# ---------------- BANK CHOICES ----------------
BANK_CHOICES = [
    ("KCB", "Kenya Commercial Bank (KCB)"),
    ("COOP", "Co-operative Bank of Kenya"),
    # International banks
    ("HSBC", "HSBC"),
    ("CITIBANK", "Citibank"),
    ("DEUTSCHE", "Deutsche Bank"),

    # US top 5
    ("CHASE", "JPMorgan Chase"),
    ("BANKOFAMERICA", "Bank of America"),
    ("USBANK", "U.S. Bank"),
]


class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallets")
    currency = models.CharField(max_length=20, choices=CRYPTO_CHOICES)
    balance = models.DecimalField(max_digits=24, decimal_places=8, default=Decimal("0.0"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "currency")

    def __str__(self):
        return f"{self.user} {self.currency} {self.balance}"


class Transaction(models.Model):
    KIND_DEBIT = "debit"
    KIND_CREDIT = "credit"
    KIND_CHOICES = [(KIND_DEBIT, "Debit"), (KIND_CREDIT, "Credit")]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.currency} {self.kind} {self.amount}"


class BankAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bank_accounts")
    bank_name = models.CharField(max_length=50, choices=BANK_CHOICES)
    account_holder_name = models.CharField(max_length=200, default="N/A", blank=True)
    account_number = models.CharField(max_length=100, default="N/A", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_preferred = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_bank_name_display()} - ****{self.account_number[-4:]}"


class Withdrawal(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="withdrawals")
    bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    crypto_amount = models.DecimalField(max_digits=24, decimal_places=8)
    fiat_amount = models.DecimalField(max_digits=24, decimal_places=2)
    currency = models.CharField(max_length=20, choices=CRYPTO_CHOICES)
    fiat_currency = models.CharField(max_length=10, default="USD")
    status = models.CharField(max_length=20, default="pending")
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdraw {self.crypto_amount} {self.currency} -> {self.fiat_amount} {self.fiat_currency}"
