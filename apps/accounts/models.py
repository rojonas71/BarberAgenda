from django.conf import settings
from django.db import models

from apps.barbershops.models import Barbershop


class Membership(models.Model):
    ROLE_DEV = "dev"
    ROLE_OWNER = "owner"
    ROLE_MANAGER = "manager"
    ROLE_RECEPTIONIST = "receptionist"
    ROLE_PROFESSIONAL = "professional"

    ROLE_CHOICES = [
        (ROLE_DEV, "Dev"),
        (ROLE_OWNER, "Proprietário"),
        (ROLE_MANAGER, "Gerente"),
        (ROLE_RECEPTIONIST, "Recepcionista"),
        (ROLE_PROFESSIONAL, "Profissional"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    barbershop = models.ForeignKey(
        Barbershop,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "barbershop",
                ],
                name="unique_membership",
            )
        ]

    @property
    def is_dev(self):
        return self.role == self.ROLE_DEV

    @property
    def can_manage_barbershop(self):
        return self.role in {
            "dev",
            "owner",
            "manager",
        }

    @property
    def can_manage_services(self):
        return self.role in {
            "dev",
            "owner",
            "manager",
        }

    @property
    def can_manage_professionals(self):
        return self.role in {
            "dev",
            "owner",
            "manager",
        }

    @property
    def can_manage_customers(self):
        return self.role in {
            "dev",
            "owner",
            "manager",
            "receptionist",
        }

    @property
    def can_manage_bookings(self):
        return self.role in {
            "dev",
            "owner",
            "manager",
            "receptionist",
        }

    @property
    def can_manage_subscription(self):
        return self.role in {
            "dev",
            "owner",
        }

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.barbershop} - "
            f"{self.get_role_display()}"
        )

@property
def can_manage_subscription(self):
    return self.role in {
        self.ROLE_DEV,
        self.ROLE_OWNER,
    }


@property
def can_manage_team(self):
    return self.role in {
        self.ROLE_DEV,
        self.ROLE_OWNER,
        self.ROLE_MANAGER,
    }


@property
def can_view_reports(self):
    return self.role in {
        self.ROLE_DEV,
        self.ROLE_OWNER,
        self.ROLE_MANAGER,
    }