from django.db import models


class Barbershop(models.Model):
    name = models.CharField(
        max_length=150,
    )

    slug = models.SlugField(
        unique=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=2,
        blank=True,
    )

    logo = models.ImageField(
        upload_to="barbershops/",
        blank=True,
        null=True,
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