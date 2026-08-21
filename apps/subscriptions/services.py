from datetime import timedelta

from django.utils import timezone

from .models import Plan, Subscription


def create_trial(barbershop):
    plan = (
        Plan.objects
        .filter(
            slug="basico",
            active=True,
        )
        .first()
    )

    if not plan:
        return None

    subscription, created = (
        Subscription.objects.get_or_create(
            barbershop=barbershop,
            defaults={
                "plan": plan,
                "status": "trial",
                "trial_ends_at": (
                    timezone.now()
                    + timedelta(days=7)
                ),
            },
        )
    )

    return subscription

def subscription_is_valid(barbershop):
    try:
        subscription = barbershop.subscription
    except Subscription.DoesNotExist:
        return False

    if subscription.status == "active":
        return True

    if (
        subscription.status == "trial"
        and subscription.trial_ends_at
        and subscription.trial_ends_at >= timezone.now()
    ):
        return True

    return False