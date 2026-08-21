from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def barbershop_required(view_func):

    @wraps(view_func)
    def wrapper(
        request,
        *args,
        **kwargs,
    ):
        if not request.user.is_authenticated:
            return redirect(
                "login"
            )

        if not getattr(
            request,
            "barbershop",
            None,
        ):
            return redirect(
                "onboarding:start"
            )

        return view_func(
            request,
            *args,
            **kwargs,
        )

    return wrapper


def permission_required(
    permission_name
):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(
            request,
            *args,
            **kwargs,
        ):
            if request.user.is_superuser:
                return view_func(
                    request,
                    *args,
                    **kwargs,
                )

            membership = getattr(
                request,
                "membership",
                None,
            )

            if not membership:
                return redirect(
                    "dashboard:home"
                )

            if membership.is_dev:
                return view_func(
                    request,
                    *args,
                    **kwargs,
                )

            allowed = getattr(
                membership,
                permission_name,
                False,
            )

            if not allowed:
                messages.error(
                    request,
                    "Você não possui permissão.",
                )

                return redirect(
                    "dashboard:home"
                )

            return view_func(
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator