from django.urls import path

from . import views


app_name = "saas_admin"


urlpatterns = [
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "barbearias/",
        views.barbershops,
        name="barbershops",
    ),

    path(
        "usuarios/",
        views.users,
        name="users",
    ),

    path(
        "planos/",
        views.plans,
        name="plans",
    ),

    path(
        "assinaturas/",
        views.subscriptions,
        name="subscriptions",
    ),

    path(
        "trials/",
        views.trials,
        name="trials",
    ),

    path(
        "logs/",
        views.logs,
        name="logs",
    ),
]