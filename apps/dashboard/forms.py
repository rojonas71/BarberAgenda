from django import forms
from django.contrib.auth import get_user_model

from apps.accounts.models import Membership
from apps.bookings.models import ScheduleBlock
from apps.professionals.models import (
    Professional,
    WorkSchedule,
)
from apps.services.models import Service


User = get_user_model()


# =========================================================
# SERVIÇOS
# =========================================================

class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service

        fields = [
            "name",
            "description",
            "price",
            "duration_minutes",
            "active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ex.: Corte masculino",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Descrição do serviço",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "duration_minutes": forms.NumberInput(
                attrs={
                    "min": "5",
                    "step": "5",
                }
            ),
        }


# =========================================================
# PROFISSIONAIS
# =========================================================

class ProfessionalForm(forms.ModelForm):

    class Meta:
        model = Professional

        fields = [
            "name",
            "phone",
            "photo",
            "services",
            "active",
        ]

        widgets = {
            "services": forms.CheckboxSelectMultiple(),
        }

    def __init__(
        self,
        *args,
        barbershop=None,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        if barbershop:
            self.fields["services"].queryset = (
                Service.objects
                .filter(
                    barbershop=barbershop,
                    active=True,
                )
                .order_by("name")
            )


# =========================================================
# HORÁRIOS
# =========================================================

class WorkScheduleForm(forms.ModelForm):

    class Meta:
        model = WorkSchedule

        fields = [
            "professional",
            "weekday",
            "start_time",
            "end_time",
            "interval_minutes",
            "active",
        ]

        widgets = {
            "start_time": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),

            "interval_minutes": forms.NumberInput(
                attrs={
                    "min": "5",
                    "step": "5",
                }
            ),
        }

    def __init__(
        self,
        *args,
        barbershop=None,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        if barbershop:
            self.fields[
                "professional"
            ].queryset = (
                Professional.objects
                .filter(
                    barbershop=barbershop,
                    active=True,
                )
                .order_by("name")
            )

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get(
            "start_time"
        )

        end_time = cleaned_data.get(
            "end_time"
        )

        if (
            start_time
            and end_time
            and start_time >= end_time
        ):
            raise forms.ValidationError(
                "O horário final deve ser maior que o inicial."
            )

        return cleaned_data


# =========================================================
# BLOQUEIOS
# =========================================================

class ScheduleBlockForm(forms.ModelForm):

    class Meta:
        model = ScheduleBlock

        fields = [
            "professional",
            "date",
            "start_time",
            "end_time",
            "reason",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),

            "reason": forms.TextInput(
                attrs={
                    "placeholder": (
                        "Ex.: Almoço, folga, férias "
                        "ou compromisso"
                    ),
                }
            ),
        }

    def __init__(
        self,
        *args,
        barbershop=None,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        if barbershop:
            self.fields[
                "professional"
            ].queryset = (
                Professional.objects
                .filter(
                    barbershop=barbershop,
                    active=True,
                )
                .order_by("name")
            )

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get(
            "start_time"
        )

        end_time = cleaned_data.get(
            "end_time"
        )

        if (
            start_time
            and end_time
            and start_time >= end_time
        ):
            raise forms.ValidationError(
                "O horário final deve ser maior que o inicial."
            )

        return cleaned_data


# =========================================================
# EQUIPE
# =========================================================

class TeamMemberForm(forms.Form):

    first_name = forms.CharField(
        label="Nome",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome do membro",
            }
        ),
    )

    username = forms.CharField(
        label="Usuário",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome de usuário",
            }
        ),
    )

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "email@exemplo.com",
            }
        ),
    )

    password = forms.CharField(
        label="Senha inicial",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha inicial",
            }
        ),
    )

    role = forms.ChoiceField(
        label="Perfil",
        choices=Membership.ROLE_CHOICES,
    )

    def clean_username(self):
        username = self.cleaned_data[
            "username"
        ]

        if User.objects.filter(
            username__iexact=username
        ).exists():
            raise forms.ValidationError(
                "Este nome de usuário já está em uso."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data[
            "email"
        ]

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Já existe um usuário com este e-mail."
            )

        return email