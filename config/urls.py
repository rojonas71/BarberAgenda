from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "",
        include("apps.public.urls"),
    ),

    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),

    path(
        "dashboard/",
        include("apps.dashboard.urls"),
    ),

    path(
        "b/",
        include("apps.bookings.urls"),
    ),

    path(
        "onboarding/",
        include("apps.onboarding.urls"),
    ),

    path(
        "super-admin/",
        include("apps.saas_admin.urls"),
    ),

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