"""
Django settings for learnlang project.
Best-practice layout for Django 5.x + allauth + WhiteNoise + dj-database-url.
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import dj_database_url

# -----------------------------------------------------------------------------
# Load .env early if present
# -----------------------------------------------------------------------------
if os.path.exists(".env"):
    # Optional module some templates use; safe to import if you have it
    try:
        import env  # noqa: F401
    except Exception:
        pass
    load_dotenv()

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "languages", "templates")

# -----------------------------------------------------------------------------
# Core config
# -----------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE-ME-UNSAFE")

# DEBUG from env (defaults to True for local dev)
DEBUG = str(os.getenv("DEBUG", "True")).lower() == "true"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "https://learnlang-e0549c82066a.herokuapp.com"]
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",   # added
    "http://localhost:8000",
    "http://localhost:8001",   # added
]

host = os.getenv("ALLOWED_HOSTS")
if host:
    ALLOWED_HOSTS.append(host)
    # Use HTTP for local/dev to avoid HTTPS/HSTS problems; HTTPS only in real prod
    IS_LOCAL = os.getenv("IS_LOCAL", "").lower() == "true"
    scheme = "https" if (not DEBUG and not IS_LOCAL) else "http"
    CSRF_TRUSTED_ORIGINS.append(f"{scheme}://{host}")

# -----------------------------------------------------------------------------
# Apps
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # required by allauth

    # Third-party
    "allauth",
    "allauth.account",

    # Local apps
    "languages",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # per WhiteNoise docs
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "learnlang.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "learnlang.wsgi.application"

# -----------------------------------------------------------------------------
# Database (SQLite for dev/test; Postgres in prod via DATABASE_URL)
# -----------------------------------------------------------------------------
if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# -----------------------------------------------------------------------------
# I18N / TZ
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static & Media
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Optional local static dir
STATIC_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [STATIC_DIR] if STATIC_DIR.exists() else []

# New-style STORAGES (Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # WhiteNoise manifest pipeline for production
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# -----------------------------------------------------------------------------
# Auth / allauth
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1

LOGIN_URL = "account_login"
# Your view is named post_login_redirect, so point to it:
LOGIN_REDIRECT_URL = "post_login_redirect"
LOGOUT_REDIRECT_URL = "account_login"

# Minimal, username-only auth (no email verification)
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_VERIFICATION = "none"
# Allow GET logout for simple navbar link (optional)
ACCOUNT_LOGOUT_ON_GET = True

# Generate http links locally (avoids https redirects in dev)
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"

# -----------------------------------------------------------------------------
# Security / HTTPS behavior
# -----------------------------------------------------------------------------
# after DEBUG is computed
IS_LOCAL = os.getenv("IS_LOCAL", "").lower() == "true"

if not DEBUG and not IS_LOCAL:
    # Production hardening
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    # Local dev/test: keep everything HTTP
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# -----------------------------------------------------------------------------
# Messages / Logging
# -----------------------------------------------------------------------------
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# -----------------------------------------------------------------------------
# Test-only overrides
# Use simple staticfiles storage during tests so collectstatic/manifest not needed
# -----------------------------------------------------------------------------
if "test" in sys.argv:
    STORAGES["staticfiles"]["BACKEND"] = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    # Make tests behave like local dev
    DEBUG = True
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# -----------------------------------------------------------------------------
# Only for testing/demo: allow embedding (turn off in real prod)
# -----------------------------------------------------------------------------
X_FRAME_OPTIONS = "ALLOWALL"
