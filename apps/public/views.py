# apps/public/views.py

from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import NoReverseMatch, reverse
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods

from apps.accounts.models import Membership
from apps.barbershops.models import Barbershop

from .forms import RegisterForm


# ============================================================
# HELPERS
# ============================================================


def model_has_field(model, field_name):
    """
    Retorna True quando o model possui determinado campo.
    """

    try:
        model._meta.get_field(field_name)
        return True
    except Exception:
        return False


def create_unique_barbershop_slug(name):
    """
    Cria um slug único para a página pública da barbearia.

    Exemplo:
        Barbearia Central
        -> barbearia-central

    Se já existir:
        -> barbearia-central-2
        -> barbearia-central-3
    """

    base_slug = slugify(name)

    if not base_slug:
        base_slug = "barbearia"

    slug = base_slug
    counter = 2

    while Barbershop.objects.filter(
        slug=slug
    ).exists():

        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


def create_barbershop_for_user(
    *,
    user,
    barbershop_name,
    phone,
):
    """
    Cria a barbearia vinculada ao usuário.

    A função verifica alguns campos opcionais para não quebrar
    caso o model Barbershop tenha estrutura diferente.
    """

    barbershop_data = {
        "name": barbershop_name,
    }

    # Slug
    if model_has_field(
        Barbershop,
        "slug",
    ):
        barbershop_data["slug"] = (
            create_unique_barbershop_slug(
                barbershop_name
            )
        )

    # WhatsApp
    if model_has_field(
        Barbershop,
        "whatsapp",
    ):
        barbershop_data["whatsapp"] = phone

    # Telefone
    elif model_has_field(
        Barbershop,
        "phone",
    ):
        barbershop_data["phone"] = phone

    # Proprietário direto no model,
    # caso exista esse campo.
    if model_has_field(
        Barbershop,
        "owner",
    ):
        barbershop_data["owner"] = user

    # Algumas versões do model usam active.
    if model_has_field(
        Barbershop,
        "active",
    ):
        barbershop_data["active"] = True

    barbershop = Barbershop.objects.create(
        **barbershop_data
    )

    return barbershop


def create_owner_membership(
    *,
    user,
    barbershop,
):
    """
    Vincula o novo usuário à barbearia como Proprietário.
    """

    role_owner = getattr(
        Membership,
        "ROLE_OWNER",
        "owner",
    )

    membership_data = {
        "user": user,
        "barbershop": barbershop,
        "role": role_owner,
    }

    # Dependendo da versão do model,
    # pode existir active ou is_active.
    if model_has_field(
        Membership,
        "active",
    ):
        membership_data["active"] = True

    elif model_has_field(
        Membership,
        "is_active",
    ):
        membership_data["is_active"] = True

    membership = Membership.objects.create(
        **membership_data
    )

    return membership


def create_trial_if_available(
    barbershop,
):
    """
    Tenta iniciar o trial de 7 dias.

    O cadastro não quebra caso o serviço de assinatura
    ainda não tenha sido criado.
    """

    try:
        from apps.subscriptions.services import (
            create_trial,
        )

    except ImportError:
        return None

    try:
        return create_trial(barbershop)

    except Exception:
        # O trial não deve impedir a criação da conta.
        return None


def get_post_register_redirect():
    """
    Prioridade:
        onboarding:start
        dashboard:home
    """

    try:
        return reverse(
            "onboarding:start"
        )

    except NoReverseMatch:
        return reverse(
            "dashboard:home"
        )


# ============================================================
# HOME / LANDING PAGE
# ============================================================


@require_http_methods(["GET"])
def home(request):
    """
    Landing page oficial do BarberAgenda.
    """

    context = {
        "page_title": (
            "BarberAgenda | Sistema para Barbearias"
        ),
        "meta_description": (
            "Sistema completo de gestão e "
            "agendamento online para barbearias."
        ),
        "trial_days": 7,
    }

    return render(
        request,
        "public/home.html",
        context,
    )


# ============================================================
# PLANOS
# ============================================================


@require_http_methods(["GET"])
def plans(request):
    """
    Página comercial de planos.
    """

    plans_data = [
        {
            "name": "Básico",
            "slug": "basico",
            "price": "49,90",
            "description": (
                "Para barbearias que estão começando."
            ),
            "featured": False,
            "features": [
                "Agenda online",
                "Agendamento público",
                "Cadastro de clientes",
                "Cadastro de serviços",
                "Até 2 profissionais",
                "Página pública da barbearia",
            ],
        },

        {
            "name": "Profissional",
            "slug": "profissional",
            "price": "79,90",
            "description": (
                "Para barbearias em crescimento."
            ),
            "featured": True,
            "features": [
                "Tudo do plano Básico",
                "Até 5 profissionais",
                "CRM de clientes",
                "Gestão de equipe",
                "Bloqueios de agenda",
                "Relatórios avançados",
            ],
        },

        {
            "name": "Premium",
            "slug": "premium",
            "price": "129,90",
            "description": (
                "Para operações profissionais."
            ),
            "featured": False,
            "features": [
                "Tudo do Profissional",
                "Até 20 profissionais",
                "CRM completo",
                "Relatórios completos",
                "Gestão de permissões",
                "Suporte prioritário",
            ],
        },
    ]

    context = {
        "page_title": (
            "Planos | BarberAgenda"
        ),
        "meta_description": (
            "Conheça os planos do BarberAgenda."
        ),
        "plans": plans_data,
        "trial_days": 7,
    }

    return render(
        request,
        "public/plans.html",
        context,
    )


# ============================================================
# CADASTRO SAAS
# ============================================================


@require_http_methods(
    [
        "GET",
        "POST",
    ]
)
def register(request):
    """
    Cadastro SaaS completo.

    Fluxo:

        Usuário
            ↓
        Barbearia
            ↓
        Membership = Proprietário
            ↓
        Trial de 7 dias
            ↓
        Login automático
            ↓
        Onboarding / Dashboard
    """

    # --------------------------------------------------------
    # USUÁRIO JÁ LOGADO
    # --------------------------------------------------------

    if request.user.is_authenticated:
        return redirect(
            "dashboard:home"
        )

    # --------------------------------------------------------
    # PLANO ESCOLHIDO
    # --------------------------------------------------------

    selected_plan = (
        request.GET
        .get(
            "plano",
            "profissional",
        )
        .strip()
        .lower()
    )

    allowed_plans = {
        "basico",
        "profissional",
        "premium",
    }

    if selected_plan not in allowed_plans:
        selected_plan = "profissional"

    # --------------------------------------------------------
    # POST
    # --------------------------------------------------------

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            try:

                # --------------------------------------------
                # TRANSAÇÃO
                # --------------------------------------------

                with transaction.atomic():

                    # ----------------------------------------
                    # USER
                    # ----------------------------------------

                    user = form.save()

                    # ----------------------------------------
                    # DADOS DA BARBEARIA
                    # ----------------------------------------

                    barbershop_name = (
                        form.cleaned_data[
                            "barbershop_name"
                        ]
                    )

                    phone = (
                        form.cleaned_data[
                            "phone"
                        ]
                    )

                    # ----------------------------------------
                    # BARBEARIA
                    # ----------------------------------------

                    barbershop = (
                        create_barbershop_for_user(
                            user=user,
                            barbershop_name=(
                                barbershop_name
                            ),
                            phone=phone,
                        )
                    )

                    # ----------------------------------------
                    # MEMBERSHIP / OWNER
                    # ----------------------------------------

                    create_owner_membership(
                        user=user,
                        barbershop=barbershop,
                    )

                    # ----------------------------------------
                    # TRIAL
                    # ----------------------------------------

                    create_trial_if_available(
                        barbershop
                    )

                # --------------------------------------------
                # LOGIN
                # --------------------------------------------

                login(
                    request,
                    user,
                )

                # --------------------------------------------
                # SUCESSO
                # --------------------------------------------

                messages.success(
                    request,
                    (
                        "Sua conta foi criada com sucesso! "
                        "Bem-vindo ao BarberAgenda."
                    ),
                )

                # --------------------------------------------
                # REDIRECT
                # --------------------------------------------

                return redirect(
                    get_post_register_redirect()
                )

            except Exception as error:

                # Desenvolvimento:
                # mostra erro útil no console.
                print(
                    "ERRO NO CADASTRO:",
                    repr(error),
                )

                messages.error(
                    request,
                    (
                        "Não foi possível concluir "
                        "seu cadastro. "
                        "Tente novamente."
                    ),
                )

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    else:

        form = RegisterForm()

    # --------------------------------------------------------
    # CONTEXTO
    # --------------------------------------------------------

    context = {
        "page_title": (
            "Criar conta | BarberAgenda"
        ),
        "meta_description": (
            "Crie sua conta e comece seu "
            "teste grátis no BarberAgenda."
        ),
        "form": form,
        "selected_plan": selected_plan,
        "trial_days": 7,
    }

    return render(
        request,
        "public/register.html",
        context,
    )


# ============================================================
# PÓS-LOGIN
# ============================================================


@require_http_methods(["GET"])
def after_login(request):
    """
    Redirecionamento inteligente após autenticação.
    """

    if not request.user.is_authenticated:
        return redirect(
            "login"
        )

    # --------------------------------------------------------
    # DEV / SUPER ADMIN
    # --------------------------------------------------------

    if request.user.is_superuser:

        try:
            return redirect(
                "saas_admin:dashboard"
            )

        except NoReverseMatch:
            return redirect(
                "dashboard:home"
            )

    # --------------------------------------------------------
    # MEMBERSHIP
    # --------------------------------------------------------

    membership = (
        Membership.objects
        .filter(
            user=request.user,
        )
        .select_related(
            "barbershop",
        )
        .first()
    )

    # Sem empresa vinculada
    if not membership:

        try:
            return redirect(
                "onboarding:start"
            )

        except NoReverseMatch:
            return redirect(
                "dashboard:home"
            )

    # --------------------------------------------------------
    # ROLE
    # --------------------------------------------------------

    role = getattr(
        membership,
        "role",
        "",
    )

    # Profissional
    professional_roles = {
        "professional",
        "profissional",
    }

    if role in professional_roles:

        try:
            return redirect(
                "dashboard:calendar"
            )

        except NoReverseMatch:
            return redirect(
                "dashboard:home"
            )

    # Recepcionista
    receptionist_roles = {
        "receptionist",
        "recepcionista",
    }

    if role in receptionist_roles:

        try:
            return redirect(
                "dashboard:calendar"
            )

        except NoReverseMatch:
            return redirect(
                "dashboard:home"
            )

    # Owner / Manager / outros
    return redirect(
        "dashboard:home"
    )


# ============================================================
# TERMOS DE USO
# ============================================================


@require_http_methods(["GET"])
def terms(request):

    context = {
        "page_title": (
            "Termos de Uso | BarberAgenda"
        ),
        "meta_description": (
            "Termos de uso da plataforma BarberAgenda."
        ),
    }

    return render(
        request,
        "public/terms.html",
        context,
    )


# ============================================================
# POLÍTICA DE PRIVACIDADE
# ============================================================


@require_http_methods(["GET"])
def privacy(request):

    context = {
        "page_title": (
            "Política de Privacidade | BarberAgenda"
        ),
        "meta_description": (
            "Política de privacidade "
            "da plataforma BarberAgenda."
        ),
    }

    return render(
        request,
        "public/privacy.html",
        context,
    )