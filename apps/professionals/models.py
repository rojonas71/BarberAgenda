from django.db import models

from apps.barbershops.models import Barbershop
from apps.services.models import Service


class Professional(models.Model):
    barbershop = models.ForeignKey(
        Barbershop,
        on_delete=models.CASCADE,
        related_name="professionals",
    )

    name = models.CharField(
        max_length=150,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    photo = models.ImageField(
        upload_to="professionals/",
        blank=True,
        null=True,
    )

    services = models.ManyToManyField(
        Service,
        related_name="professionals",
        blank=True,
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

    def __str__(self):
        return self.name


class WorkSchedule(models.Model):
    WEEKDAYS = [
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="work_schedules",
    )

    weekday = models.PositiveSmallIntegerField(
        choices=WEEKDAYS,
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    interval_minutes = models.PositiveIntegerField(
        default=30,
    )

    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return (
            f"{self.professional} - "
            f"{self.get_weekday_display()}"
        )