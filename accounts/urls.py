from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("banks/", views.banks, name="banks"),
    path("bank/add/", views.add_bank_account, name="add_bank"),
    path("bank/set-preferred/", views.set_preferred_bank, name="set_preferred_bank"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transactions/", views.transactions, name="transactions"),
]

