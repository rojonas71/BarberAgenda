from django.urls import path

from . import views


app_name = "public"


urlpatterns = [
    path(
        "",
        views.landing_page,
        name="home",
    ),

    path(
        "cadastro/",
        views.register,
        name="register",
    ),

    path(
        "planos/",
        views.plans,
        name="plans",
    ),
]