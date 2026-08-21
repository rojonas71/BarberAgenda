from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome",
        max_length=150,
    )

    email = forms.EmailField(
        label="E-mail",
        required=True,
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Já existe uma conta com este e-mail."
            )

        return email

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Seu nome",
                "autocomplete": "name",
            }
        ),
    )

    username = forms.CharField(
        label="Usuário",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Escolha um nome de usuário",
                "autocomplete": "username",
            }
        ),
    )

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "voce@email.com",
                "autocomplete": "email",
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = (
            self.cleaned_data["username"]
            .strip()
        )

        if User.objects.filter(
            username__iexact=username
        ).exists():
            raise forms.ValidationError(
                "Este nome de usuário já está em uso."
            )

        return username

    def clean_email(self):
        email = (
            self.cleaned_data["email"]
            .strip()
            .lower()
        )

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Já existe uma conta cadastrada com este e-mail."
            )

        return email

    def save(self, commit=True):
        user = super().save(
            commit=False
        )

        user.first_name = (
            self.cleaned_data["first_name"]
            .strip()
        )

        user.username = (
            self.cleaned_data["username"]
            .strip()
        )

        user.email = (
            self.cleaned_data["email"]
            .strip()
            .lower()
        )

        if commit:
            user.save()

        return user