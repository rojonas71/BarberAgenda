from django.urls import path

from . import views


app_name = "bookings"


urlpatterns = [
    path(
        "<slug:slug>/",
        views.booking_home,
        name="home",
    ),

    path(
        "<slug:slug>/agendar/",
        views.create_booking,
        name="create",
    ),

    path(
        "<slug:slug>/horarios/",
        views.available_slots,
        name="available_slots",
    ),
]