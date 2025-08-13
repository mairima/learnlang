"""
Django settings for learnlang project.
Best-practice layout for Django 5.x + allauth + WhiteNoise + dj-database-url.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
if os.path.exists(".env"):
    import env  # noqa: F401
    load_dotenv()  # load .env if present

# ------------------------------------------------------------------------------
# Paths & env
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "languages", "templates")

# ------------------------------------------------------------------------------
# Core config
# ------------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE-ME-UNSAFE")
DEBUG = os.getenv("DEBUG", False)

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []
host= os.getenv(
    "ALLOWED_HOSTS"
)
if host:
    ALLOWED_HOSTS.append(host)
    CSRF_TRUSTED_ORIGINS.append(f"https://{host}")

# ------------------------------------------------------------------------------
# Apps
# ------------------------------------------------------------------------------
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
        # Add a top-level /templates dir if you have one:
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # required by allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "learnlang.wsgi.application"

# ------------------------------------------------------------------------------
# Database (SQLite for dev; Postgres via DATABASE_URL in prod)
# ------------------------------------------------------------------------------
if os.getenv("DATABASE_URL"):
    # Example: postgres://USER:PASSWORD@HOST:PORT/DBNAME
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,  # keep connections for performance
            ssl_require=not DEBUG,  # require SSL in production
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ------------------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------------------
# I18N / TZ
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# Static & Media
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# If you have a local "static" folder for source assets:
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

# New-style STORAGES (Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # WhiteNoise pipeline with hashed filenames + compression
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ------------------------------------------------------------------------------
# Auth / allauth
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "after_login"   # implement your role-based router
LOGOUT_REDIRECT_URL = "account_login"

# Minimal, username-only auth (no email verification)
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_VERIFICATION = "none"

# Allow GET logout for simple navbar link (optional convenience)
ACCOUNT_LOGOUT_ON_GET = True

# ------------------------------------------------------------------------------
# Security (production hardening)
# ------------------------------------------------------------------------------
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_SSL_REDIRECT = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ------------------------------------------------------------------------------
# Messages / Logging
# ------------------------------------------------------------------------------
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": True},
        "django.security": {"handlers": ["console"], "level": "ERROR", "propagate": True},
    },
}
