from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.shortcuts import render

from apps.barbershops.models import Barbershop
from apps.subscriptions.models import Plan, Subscription

from .models import AuditLog


User = get_user_model()


def is_platform_admin(user):
    return (
        user.is_authenticated
        and user.is_superuser
    )


@user_passes_test(is_platform_admin)
def dashboard(request):

    total_barbershops = (
        Barbershop.objects.count()
    )

    active_barbershops = (
        Barbershop.objects
        .filter(active=True)
        .count()
    )

    total_users = User.objects.count()

    active_subscriptions = (
        Subscription.objects
        .filter(status="active")
        .count()
    )

    trials = (
        Subscription.objects
        .filter(status="trial")
        .count()
    )

    mrr = (
        Subscription.objects
        .filter(status="active")
        .aggregate(
            total=Sum("plan__price")
        )
        .get("total")
        or 0
    )

    context = {
        "total_barbershops":
            total_barbershops,

        "active_barbershops":
            active_barbershops,

        "total_users":
            total_users,

        "active_subscriptions":
            active_subscriptions,

        "trials":
            trials,

        "mrr":
            mrr,
    }

    return render(
        request,
        "saas_admin/dashboard.html",
        context,
    )


@user_passes_test(is_platform_admin)
def barbershops(request):

    barbershop_list = (
        Barbershop.objects
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "saas_admin/barbershops.html",
        {
            "barbershops":
                barbershop_list,
        },
    )


@user_passes_test(is_platform_admin)
def users(request):

    user_list = (
        User.objects
        .all()
        .order_by("-date_joined")
    )

    return render(
        request,
        "saas_admin/users.html",
        {
            "users": user_list,
        },
    )


@user_passes_test(is_platform_admin)
def plans(request):

    plan_list = (
        Plan.objects
        .all()
        .order_by("price")
    )

    return render(
        request,
        "saas_admin/plans.html",
        {
            "plans": plan_list,
        },
    )


@user_passes_test(is_platform_admin)
def subscriptions(request):

    subscription_list = (
        Subscription.objects
        .select_related(
            "barbershop",
            "plan",
        )
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "saas_admin/subscriptions.html",
        {
            "subscriptions":
                subscription_list,
        },
    )


@user_passes_test(is_platform_admin)
def trials(request):

    trial_list = (
        Subscription.objects
        .filter(status="trial")
        .select_related(
            "barbershop",
            "plan",
        )
        .order_by("trial_ends_at")
    )

    return render(
        request,
        "saas_admin/trials.html",
        {
            "trials": trial_list,
        },
    )


@user_passes_test(is_platform_admin)
def logs(request):

    log_list = (
        AuditLog.objects
        .select_related("user")
        .all()[:200]
    )

    return render(
        request,
        "saas_admin/logs.html",
        {
            "logs": log_list,
        },
    )