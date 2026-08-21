from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.text import slugify

from apps.accounts.models import Membership
from apps.barbershops.models import Barbershop

from .forms import BarbershopOnboardingForm


@login_required
def start(request):
    existing_membership = (
        Membership.objects
        .filter(
            user=request.user,
            active=True,
        )
        .select_related("barbershop")
        .first()
    )

    if existing_membership:
        return redirect(
            "dashboard:home"
        )

    if request.method == "POST":
        form = BarbershopOnboardingForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            barbershop = form.save(
                commit=False
            )

            base_slug = slugify(
                barbershop.name
            )

            slug = base_slug
            counter = 2

            while Barbershop.objects.filter(
                slug=slug
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            barbershop.slug = slug
            barbershop.active = True
            barbershop.save()

            Membership.objects.create(
                user=request.user,
                barbershop=barbershop,
                role=Membership.ROLE_OWNER,
                active=True,
            )

            return redirect(
                "dashboard:home"
            )

    else:
        form = BarbershopOnboardingForm()

    return render(
        request,
        "onboarding/start.html",
        {
            "form": form,
        },
    )