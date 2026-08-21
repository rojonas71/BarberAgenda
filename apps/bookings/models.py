import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.barbershops.models import Barbershop
from apps.customers.models import Customer
from apps.professionals.models import Professional
from apps.services.models import Service


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("confirmed", "Confirmado"),
        ("completed", "Concluído"),
        ("cancelled", "Cancelado"),
        ("no_show", "Não compareceu"),
    ]

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    barbershop = models.ForeignKey(
        Barbershop,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    professional = models.ForeignKey(
        Professional,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(
                "Horário final deve ser maior que o inicial."
            )

        conflicts = Booking.objects.filter(
            professional=self.professional,
            date=self.date,
            status__in=[
                "pending",
                "confirmed",
            ],
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )

        if self.pk:
            conflicts = conflicts.exclude(
                pk=self.pk
            )

        if conflicts.exists():
            raise ValidationError(
                "Já existe um agendamento neste horário."
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(
            *args,
            **kwargs
        )

    def __str__(self):
        return (
            f"{self.customer} - "
            f"{self.date} "
            f"{self.start_time}"
        )


class ScheduleBlock(models.Model):
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="schedule_blocks",
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    reason = models.CharField(
        max_length=200,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(
                "Horário final inválido."
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(
            *args,
            **kwargs
        )