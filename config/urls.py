from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # allauth routes (login, signup, logout, social login, etc.)
    path("accounts/", include("allauth.urls")),

    # your custom accounts app (if you add extra views later)
    path("", include(("accounts.urls", "accounts"), namespace="accounts")),
]

# ✅ serve media in dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.BASE_DIR / "media")
