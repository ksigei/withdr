from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),   # login/signup/social login
    path("", include(("accounts.urls", "accounts"), namespace="accounts")),
]
