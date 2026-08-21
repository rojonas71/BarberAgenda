from apps.accounts.models import Membership


class CurrentBarbershopMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.barbershop = None
        request.membership = None

        if request.user.is_authenticated:
            membership = (
                Membership.objects
                .filter(
                    user=request.user,
                    active=True,
                    barbershop__active=True,
                )
                .select_related(
                    "barbershop"
                )
                .first()
            )

            if membership:
                request.membership = membership
                request.barbershop = (
                    membership.barbershop
                )

        return self.get_response(
            request
        )