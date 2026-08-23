from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # SITE PÚBLICO
    path(
        "",
        include(
            ("apps.public.urls", "public"),
            namespace="public",
        ),
    ),

    # LOGIN / SENHA
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),

    # DASHBOARD
    path(
        "dashboard/",
        include("apps.dashboard.urls"),
    ),

    # AGENDAMENTO PÚBLICO
    path(
        "b/",
        include("apps.bookings.urls"),
    ),

    # SUPER ADMIN
    path(
        "super-admin/",
        include("apps.saas_admin.urls"),
    ),

    # ADMIN DJANGO
    path(
        "admin/",
        admin.site.urls,
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )