from django import forms

from apps.barbershops.models import Barbershop


class BarbershopOnboardingForm(forms.ModelForm):

    class Meta:
        model = Barbershop

        fields = [
            "name",
            "phone",
            "whatsapp",
            "address",
            "city",
            "state",
            "logo",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder":
                        "Nome da sua barbearia",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder":
                        "(17) 00000-0000",
                }
            ),

            "whatsapp": forms.TextInput(
                attrs={
                    "placeholder":
                        "(17) 99999-9999",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "placeholder":
                        "Endereço da barbearia",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder":
                        "Cidade",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "placeholder": "SP",
                    "maxlength": 2,
                }
            ),
        }