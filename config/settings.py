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


# ============================================================
# HOSTS
# ============================================================

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "barberagenda26.onrender.com",
    "app.barberagenda.com.br",
]


# Host automático disponibilizado pelo Render
RENDER_EXTERNAL_HOSTNAME = os.getenv(
    "RENDER_EXTERNAL_HOSTNAME"
)

if (
    RENDER_EXTERNAL_HOSTNAME
    and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS
):
    ALLOWED_HOSTS.append(
        RENDER_EXTERNAL_HOSTNAME
    )


# Permite adicionar outros hosts por variável de ambiente.
#
# Exemplo:
# ALLOWED_HOSTS=barberagenda26.onrender.com,app.barberagenda.com.br
#
EXTRA_ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "",
)

if EXTRA_ALLOWED_HOSTS:
    for host in EXTRA_ALLOWED_HOSTS.split(","):
        host = host.strip()

        if (
            host
            and host not in ALLOWED_HOSTS
        ):
            ALLOWED_HOSTS.append(host)


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    "https://barberagenda26.onrender.com",
    "https://app.barberagenda.com.br",
]


if RENDER_EXTERNAL_HOSTNAME:
    render_origin = (
        f"https://{RENDER_EXTERNAL_HOSTNAME}"
    )

    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(
            render_origin
        )


# ============================================================
# APLICAÇÕES
# ============================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # BarberAgenda
    "apps.accounts.apps.AccountsConfig",
    "apps.barbershops.apps.BarbershopsConfig",
    "apps.professionals.apps.ProfessionalsConfig",
    "apps.services.apps.ServicesConfig",
    "apps.bookings.apps.BookingsConfig",
    "apps.customers.apps.CustomersConfig",
    "apps.dashboard.apps.DashboardConfig",

    # Micro SaaS
    "apps.core.apps.CoreConfig",
    "apps.subscriptions.apps.SubscriptionsConfig",

    # Super Admin
    "apps.saas_admin.apps.SaasAdminConfig",

    # Área pública
    "apps.public.apps.PublicConfig",
]


# ============================================================
# AUTENTICAÇÃO
# ============================================================

AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.EmailOrUsernameBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise deve ficar logo depois
    # do SecurityMiddleware.
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


# ============================================================
# URLS
# ============================================================

ROOT_URLCONF = "config.urls"


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
                    "django.template."
                    "context_processors.request"
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
# WSGI
# ============================================================

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "",
).strip()


if DATABASE_URL:

    # --------------------------------------------------------
    # PRODUÇÃO / RENDER
    # --------------------------------------------------------

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:

    # --------------------------------------------------------
    # DESENVOLVIMENTO LOCAL / WINDOWS
    # --------------------------------------------------------

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


STATICFILES_DIRS = []

STATIC_SOURCE_DIR = BASE_DIR / "static"

if STATIC_SOURCE_DIR.exists():
    STATICFILES_DIRS.append(
        STATIC_SOURCE_DIR
    )


STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# ============================================================
# MEDIA / UPLOADS
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# LOGIN / LOGOUT
# ============================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "public:after_login"

LOGOUT_REDIRECT_URL = "public:home"


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
# SESSÕES
# ============================================================

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False


# ============================================================
# SEGURANÇA DE PRODUÇÃO
# ============================================================

if not DEBUG:

    # Render recebe HTTPS por proxy.
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    # Força HTTPS
    SECURE_SSL_REDIRECT = True

    # Cookies somente via HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Segurança adicional
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_REFERRER_POLICY = (
        "strict-origin-when-cross-origin"
    )

    X_FRAME_OPTIONS = "DENY"


# ============================================================
# PRODUÇÃO - HSTS
# ============================================================
#
# Não habilite HSTS permanente imediatamente.
#
# Depois que:
#
# https://barberagenda26.onrender.com
#
# e
#
# https://app.barberagenda.com.br
#
# estiverem funcionando perfeitamente,
# você poderá habilitar:
#
# if not DEBUG:
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
#
# ============================================================