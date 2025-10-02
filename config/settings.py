"""
Django settings for config project.
Production-ready for Railway deployment.
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- SECURITY ----------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "changeme-in-prod")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "withdr-production.up.railway.app",
    "perpetual-growth-production-2b89.up.railway.app",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://perpetual-growth-production-2b89.up.railway.app",
    "https://withdr-production.up.railway.app",
    "https://*.railway.app",  # wildcard for Railway domains
]

# ---------------- INSTALLED APPS ----------------
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Whitenoise
    "whitenoise.runserver_nostatic",  # static in dev

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # local apps
    'accounts',
]

# ---------------- AUTH / ALLAUTH CONFIG ----------------
AUTH_USER_MODEL = "accounts.CustomUser"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_FIELDS = ["email", "password1", "password2"]
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_VERIFICATION = "none"

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_ADAPTER = "accounts.adapter.NoUsernameAccountAdapter"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "APP": {
            "client_id": "77283946027-888vrbmfhdcod1ou3nh12otkclkj208q.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        },
    }
}

# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------- URLS & WSGI ----------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",  # required by allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------- DATABASE ----------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600
    )
}

# ---------------- PASSWORD VALIDATORS ----------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------- I18N ----------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

# ---------------- STATIC & MEDIA ----------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# domains 
SITE_ID = 1

# 

# ---------------- DEFAULTS ----------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
