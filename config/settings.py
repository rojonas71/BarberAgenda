"""
Django settings for BarberAgenda.
"""

import os
from pathlib import Path

import dj_database_url


# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SEGURANÇA
# ============================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-dev-only-change-me",
)

DEBUG = os.getenv(
    "DEBUG",
    "True",
).lower() == "true"


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
    "app.barberagenda.com.br",
]


RENDER_EXTERNAL_HOSTNAME = os.getenv(
    "RENDER_EXTERNAL_HOSTNAME"
)

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(
        RENDER_EXTERNAL_HOSTNAME
    )


CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "https://app.barberagenda.com.br",
]


# ============================================================
# APPS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Projeto
    "apps.accounts.apps.AccountsConfig",
    "apps.barbershops.apps.BarbershopsConfig",
    "apps.professionals.apps.ProfessionalsConfig",
    "apps.services.apps.ServicesConfig",
    "apps.bookings.apps.BookingsConfig",
    "apps.customers.apps.CustomersConfig",
    "apps.dashboard.apps.DashboardConfig",

    # SaaS
    "apps.core.apps.CoreConfig",
    "apps.subscriptions.apps.SubscriptionsConfig",

    # Super Admin
    "apps.saas_admin.apps.SaasAdminConfig",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Static files no Render
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # BarberAgenda
    "apps.core.middleware.CurrentBarbershopMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# IMPORTANTE:
# NÃO coloque AppConfig dentro do MIDDLEWARE.
#
# ERRADO:
#
# "apps.subscriptions.apps.SubscriptionsConfig"
# "apps.onboarding.apps.OnboardingConfig"
# "apps.saas_admin.apps.SaasAdminConfig"


# ============================================================
# URLS / WSGI
# ============================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends.django."
            "DjangoTemplates"
        ),

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                (
                    "django.template.context_processors."
                    "request"
                ),
                (
                    "django.contrib.auth."
                    "context_processors.auth"
                ),
                (
                    "django.contrib.messages."
                    "context_processors.messages"
                ),
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")

import os


if os.getenv("RDS_HOSTNAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["RDS_DB_NAME"],
            "USER": os.environ["RDS_USERNAME"],
            "PASSWORD": os.environ["RDS_PASSWORD"],
            "HOST": os.environ["RDS_HOSTNAME"],
            "PORT": os.getenv(
                "RDS_PORT",
                "5432",
            ),
            "CONN_MAX_AGE": 600,
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
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


# ============================================================
# INTERNACIONALIZAÇÃO
# ============================================================

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# Caso você tenha uma pasta /static na raiz
STATICFILES_DIRS = []

if (BASE_DIR / "static").exists():
    STATICFILES_DIRS.append(
        BASE_DIR / "static"
    )


# ============================================================
# MEDIA
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# LOGIN / LOGOUT
# ============================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "dashboard:home"

LOGOUT_REDIRECT_URL = "login"


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# ============================================================
# SEGURANÇA EM PRODUÇÃO
# ============================================================

if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    X_FRAME_OPTIONS = "DENY"

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_REFERRER_POLICY = (
        "strict-origin-when-cross-origin"
    )


DEBUG = os.getenv(
    "DEBUG",
    "True",
).lower() == "true"


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-only-secret",
)


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".elasticbeanstalk.com",
    "app.barberagenda.com.br",
]


CSRF_TRUSTED_ORIGINS = [
    "https://app.barberagenda.com.br",
]

if os.getenv("RDS_HOSTNAME"):

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",

            "NAME": os.getenv(
                "RDS_DB_NAME",
                "postgres",
            ),

            "USER": os.getenv(
                "RDS_USERNAME",
            ),

            "PASSWORD": os.getenv(
                "RDS_PASSWORD",
            ),

            "HOST": os.getenv(
                "RDS_HOSTNAME",
            ),

            "PORT": os.getenv(
                "RDS_PORT",
                "5432",
            ),

            "CONN_MAX_AGE": 600,
        }
    }

else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }