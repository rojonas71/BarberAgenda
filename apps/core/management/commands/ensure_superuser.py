import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    help = "Cria ou atualiza o administrador inicial do BarberAgenda."

    def handle(self, *args, **options):
        username = os.getenv(
            "DJANGO_SUPERUSER_USERNAME",
            "",
        ).strip()

        email = os.getenv(
            "DJANGO_SUPERUSER_EMAIL",
            "",
        ).strip().lower()

        password = os.getenv(
            "DJANGO_SUPERUSER_PASSWORD",
            "",
        )

        if not username:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_USERNAME não configurado."
                )
            )
            return

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_PASSWORD não configurado."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
            },
        )

        changed = False

        if email and user.email != email:
            user.email = email
            changed = True

        if not user.is_staff:
            user.is_staff = True
            changed = True

        if not user.is_superuser:
            user.is_superuser = True
            changed = True

        if not user.is_active:
            user.is_active = True
            changed = True

        # Atualiza a senha para o valor definido no Render.
        if not user.check_password(password):
            user.set_password(password)
            changed = True

        if changed:
            user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superusuário '{username}' criado com sucesso."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superusuário '{username}' verificado/atualizado."
                )
            )