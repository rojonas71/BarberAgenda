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
                "class": "form-input",
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
                "class": "form-input",
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
                "class": "form-input",
                "placeholder": "voce@email.com",
                "autocomplete": "email",
            }
        ),
    )

    phone = forms.CharField(
        label="WhatsApp",
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "(17) 99999-9999",
                "autocomplete": "tel",
                "inputmode": "tel",
            }
        ),
    )

    barbershop_name = forms.CharField(
        label="Nome da barbearia",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Ex.: Barbearia Central",
                "autocomplete": "organization",
            }
        ),
    )

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Crie uma senha segura",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Digite a senha novamente",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "username",
            "email",
            "phone",
            "barbershop_name",
            "password1",
            "password2",
        ]

    def clean_first_name(self):
        first_name = (
            self.cleaned_data["first_name"]
            .strip()
        )

        if len(first_name) < 2:
            raise forms.ValidationError(
                "Informe um nome válido."
            )

        return first_name

    def clean_username(self):
        username = (
            self.cleaned_data["username"]
            .strip()
        )

        if len(username) < 3:
            raise forms.ValidationError(
                "O usuário deve ter pelo menos 3 caracteres."
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

    def clean_phone(self):
        phone = (
            self.cleaned_data["phone"]
            .strip()
        )

        digits = "".join(
            character
            for character in phone
            if character.isdigit()
        )

        if len(digits) < 10:
            raise forms.ValidationError(
                "Informe um WhatsApp válido."
            )

        if len(digits) > 13:
            raise forms.ValidationError(
                "Informe um WhatsApp válido."
            )

        return phone

    def clean_barbershop_name(self):
        barbershop_name = (
            self.cleaned_data["barbershop_name"]
            .strip()
        )

        if len(barbershop_name) < 2:
            raise forms.ValidationError(
                "Informe o nome da sua barbearia."
            )

        return barbershop_name

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