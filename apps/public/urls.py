from django.urls import path

from . import views


app_name = "public"


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "planos/",
        views.plans,
        name="plans",
    ),

    path(
        "cadastro/",
        views.register,
        name="register",
    ),

    path(
        "pos-login/",
        views.after_login,
        name="after_login",
    ),

    path(
        "termos/",
        views.terms,
        name="terms",
    ),

    path(
        "privacidade/",
        views.privacy,
        name="privacy",
    ),
]