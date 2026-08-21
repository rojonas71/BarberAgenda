from django.contrib.auth import login
from django.shortcuts import redirect, render

from apps.subscriptions.models import Plan

from .forms import RegisterForm


def landing_page(request):
    plans = (
        Plan.objects
        .filter(active=True)
        .order_by("price")
    )

    return render(
        request,
        "public/home.html",
        {
            "plans": plans,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect(
            "dashboard:home"
        )

    if request.method == "POST":
        form = RegisterForm(
            request.POST
        )

        if form.is_valid():
            user = form.save()

            login(
                request,
                user,
            )

            return redirect(
                "onboarding:start"
            )

    else:
        form = RegisterForm()

    return render(
        request,
        "public/register.html",
        {
            "form": form,
        },
    )


def plans(request):
    plans = (
        Plan.objects
        .filter(active=True)
        .order_by("price")
    )

    return render(
        request,
        "public/plans.html",
        {
            "plans": plans,
        },
    )

from django.contrib.auth import login
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect(
            "dashboard:home"
        )

    if request.method == "POST":
        form = RegisterForm(
            request.POST
        )

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()

            except IntegrityError:
                form.add_error(
                    "username",
                    (
                        "Este nome de usuário "
                        "já está em uso."
                    ),
                )

            else:
                login(
                    request,
                    user,
                )

                return redirect(
                    "onboarding:start"
                )

    else:
        form = RegisterForm()

    return render(
        request,
        "public/register.html",
        {
            "form": form,
        },
    )