from django.db import models

from apps.barbershops.models import Barbershop


class Plan(models.Model):

    priority_support = models.BooleanField(
     default=False,
    )
    name = models.CharField(
        max_length=100,
    )

    slug = models.SlugField(
        unique=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    max_professionals = models.PositiveIntegerField(
        default=1,
    )

    max_services = models.PositiveIntegerField(
        default=5,
    )

    max_team_members = models.PositiveIntegerField(
        default=1,
    )

    crm_enabled = models.BooleanField(
        default=False,
    )

    advanced_reports = models.BooleanField(
        default=False,
    )

    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name

    


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("trial", "Teste grátis"),
        ("active", "Ativa"),
        ("past_due", "Pagamento pendente"),
        ("cancelled", "Cancelada"),
        ("expired", "Expirada"),
    ]

    barbershop = models.OneToOneField(
        Barbershop,
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="trial",
    )

    trial_ends_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    current_period_end = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )