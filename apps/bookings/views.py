from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from apps.barbershops.models import Barbershop


def booking_home(request, slug):
    barbershop = get_object_or_404(
        Barbershop,
        slug=slug,
        active=True,
    )

    services = (
        barbershop.services
        .filter(active=True)
        .order_by("name")
    )

    professionals = (
        barbershop.professionals
        .filter(active=True)
        .prefetch_related("services")
        .order_by("name")
    )

    return render(
        request,
        "bookings/home.html",
        {
            "barbershop": barbershop,
            "services": services,
            "professionals": professionals,
        },
    )

def create_booking(request, slug):
    barbershop = get_object_or_404(
        Barbershop,
        slug=slug,
        active=True,
    )

    return render(
        request,
        "bookings/create.html",
        {
            "barbershop": barbershop,
        },
    )


def available_slots(request, slug):
    return JsonResponse(
        {
            "slots": [],
        }
    )