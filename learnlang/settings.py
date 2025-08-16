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
# Load .env early if present (local dev)
# -----------------------------------------------------------------------------
if os.path.exists(".env"):
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

# Default to False for safety (prod on Heroku)
DEBUG = str(os.getenv("DEBUG", "False")).lower() == "true"

# Helper to normalize host values (strip scheme/path)
def _clean_host(h: str) -> str:
    h = h.replace("https://", "").replace("http://", "")
    return h.split("/")[0].strip()

# Base local hosts
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Add env-driven hosts (comma or space separated)
_env_hosts = os.getenv("ALLOWED_HOSTS", "")
if _env_hosts:
    for token in _env_hosts.replace(" ", ",").split(","):
        token = token.strip()
        if token:
            host = _clean_host(token)
            if host and host not in ALLOWED_HOSTS:
                ALLOWED_HOSTS.append(host)

# CSRF trusted origins: local + env-driven (scheme depends on env)
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://localhost:8000",
    "http://localhost:8001",
]
IS_LOCAL = str(os.getenv("IS_LOCAL", "")).lower() == "true"
_scheme = "https" if (not DEBUG and not IS_LOCAL) else "http"
for host in ALLOWED_HOSTS:
    if host not in {"127.0.0.1", "localhost"}:
        CSRF_TRUSTED_ORIGINS.append(f"{_scheme}://{host}")

# -----------------------------------------------------------------------------
# Apps
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "languages",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
# Database (SQLite for dev; Postgres in prod via DATABASE_URL)
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
# Static files (WhiteNoise)
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [STATIC_DIR] if STATIC_DIR.exists() else []

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}

# -----------------------------------------------------------------------------
# Auth / allauth
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "post_login_redirect"
LOGOUT_REDIRECT_URL = "account_login"

ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"

# -----------------------------------------------------------------------------
# Security (production hardening)
# -----------------------------------------------------------------------------
if not DEBUG and not IS_LOCAL:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_CONTENT_TYPE_NOSNIFF = True
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
else:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# -----------------------------------------------------------------------------
# Messages / Logging
# -----------------------------------------------------------------------------
MESSAGE_STORAGE = (
    "django.contrib.messages.storage.session.SessionStorage"
)

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
# -----------------------------------------------------------------------------
if "test" in sys.argv:
    STORAGES["staticfiles"]["BACKEND"] = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    DEBUG = True
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
