from apps.accounts.models import Membership
from apps.professionals.models import Professional
from apps.services.models import Service


def get_subscription(barbershop):
    return getattr(
        barbershop,
        "subscription",
        None,
    )


def can_create_service(barbershop):
    subscription = get_subscription(
        barbershop
    )

    if not subscription:
        return False

    total = Service.objects.filter(
        barbershop=barbershop
    ).count()

    return (
        total
        < subscription.plan.max_services
    )


def can_create_professional(barbershop):
    subscription = get_subscription(
        barbershop
    )

    if not subscription:
        return False

    total = Professional.objects.filter(
        barbershop=barbershop
    ).count()

    return (
        total
        < subscription.plan.max_professionals
    )


def can_create_team_member(barbershop):
    subscription = get_subscription(
        barbershop
    )

    if not subscription:
        return False

    total = Membership.objects.filter(
        barbershop=barbershop,
        active=True,
    ).count()

    return (
        total
        < subscription.plan.max_team_members
    )

from apps.subscriptions.limits import (
    can_create_service,
)


if not can_create_service(
    request.barbershop
):
    messages.warning(
        request,
        "Seu plano atingiu o limite de serviços.",
    )

    return redirect(
        "dashboard:services"
    )