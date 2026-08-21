from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone
from apps.customers.models import Customer

from apps.accounts.models import Membership
from apps.bookings.models import (
    Booking,
    ScheduleBlock,
)
from apps.customers.models import Customer
from apps.core.decorators import (
    barbershop_required,
    permission_required,
)
from apps.professionals.models import (
    Professional,
    WorkSchedule,
)
from apps.services.models import Service

from .forms import (
    ProfessionalForm,
    ScheduleBlockForm,
    ServiceForm,
    TeamMemberForm,
    WorkScheduleForm,
)


User = get_user_model()


# =========================================================
# DASHBOARD
# =========================================================

@login_required
@barbershop_required
def dashboard_home(request):
    barbershop = request.barbershop
    today = timezone.localdate()

    bookings_today = (
        Booking.objects
        .filter(
            barbershop=barbershop,
            date=today,
        )
        .select_related(
            "customer",
            "service",
            "professional",
        )
        .order_by("start_time")
    )

    total_today = bookings_today.count()

    pending_today = bookings_today.filter(
        status="pending"
    ).count()

    confirmed_today = bookings_today.filter(
        status="confirmed"
    ).count()

    completed_today = bookings_today.filter(
        status="completed"
    ).count()

    cancelled_today = bookings_today.filter(
        status="cancelled"
    ).count()

    revenue_today = (
        bookings_today
        .filter(
            status="completed"
        )
        .aggregate(
            total=Sum("service__price")
        )
        .get("total")
        or 0
    )

    total_customers = (
        Customer.objects
        .filter(
            barbershop=barbershop
        )
        .count()
    )

    next_bookings = (
        bookings_today
        .filter(
            status__in=[
                "pending",
                "confirmed",
            ]
        )
        .order_by("start_time")[:5]
    )

    return render(
        request,
        "dashboard/home.html",
        {
            "today": today,
            "bookings_today": bookings_today,
            "next_bookings": next_bookings,
            "total_today": total_today,
            "pending_today": pending_today,
            "confirmed_today": confirmed_today,
            "completed_today": completed_today,
            "cancelled_today": cancelled_today,
            "revenue_today": revenue_today,
            "total_customers": total_customers,
        },
    )


# =========================================================
# AGENDA / AGENDAMENTOS
# =========================================================

@login_required
@barbershop_required
@permission_required("can_manage_bookings")
def agenda(request):
    selected_date = (
        request.GET.get("date")
        or str(timezone.localdate())
    )

    bookings = (
        Booking.objects
        .filter(
            barbershop=request.barbershop,
            date=selected_date,
        )
        .select_related(
            "customer",
            "service",
            "professional",
        )
        .order_by(
            "professional__name",
            "start_time",
        )
    )

    return render(
        request,
        "dashboard/agenda.html",
        {
            "bookings": bookings,
            "selected_date": selected_date,
        },
    )


@login_required
@barbershop_required
@permission_required("can_manage_bookings")
def booking_list(request):
    bookings = (
        Booking.objects
        .filter(
            barbershop=request.barbershop
        )
        .select_related(
            "customer",
            "service",
            "professional",
        )
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    )

    date = request.GET.get(
        "date",
        ""
    )

    professional = request.GET.get(
        "professional",
        ""
    )

    if search:
        bookings = bookings.filter(
            customer__name__icontains=search
        )

    if status:
        bookings = bookings.filter(
            status=status
        )

    if date:
        bookings = bookings.filter(
            date=date
        )

    if professional:
        bookings = bookings.filter(
            professional_id=professional
        )

    bookings = bookings.order_by(
        "-date",
        "-start_time",
    )

    professionals = (
        Professional.objects
        .filter(
            barbershop=request.barbershop,
            active=True,
        )
        .order_by("name")
    )

    return render(
        request,
        "dashboard/bookings.html",
        {
            "bookings": bookings,
            "professionals": professionals,
            "search": search,
            "selected_status": status,
            "selected_date": date,
            "selected_professional": professional,
        },
    )


@login_required
@barbershop_required
@permission_required("can_manage_bookings")
def booking_detail(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_related(
            "customer",
            "service",
            "professional",
        ),
        pk=pk,
        barbershop=request.barbershop,
    )

    return render(
        request,
        "dashboard/booking_detail.html",
        {
            "booking": booking,
        },
    )


@login_required
@barbershop_required
@permission_required("can_manage_bookings")
def booking_update_status(request, pk):
    booking = get_object_or_404(
        Booking,
        pk=pk,
        barbershop=request.barbershop,
    )

    if request.method != "POST":
        return redirect(
            "dashboard:booking_detail",
            pk=booking.pk,
        )

    status = request.POST.get("status")

    valid_statuses = {
        value
        for value, label
        in Booking.STATUS_CHOICES
    }

    if status not in valid_statuses:
        messages.error(
            request,
            "Status inválido.",
        )

        return redirect(
            "dashboard:booking_detail",
            pk=booking.pk,
        )

    booking.status = status
    booking.save()

    messages.success(
        request,
        "Status atualizado com sucesso.",
    )

    return redirect(
        "dashboard:booking_detail",
        pk=booking.pk,
    )


# =========================================================
# SERVIÇOS
# =========================================================

@login_required
@barbershop_required
def services(request):
    services = (
        Service.objects
        .filter(
            barbershop=request.barbershop
        )
        .order_by("name")
    )

    return render(
        request,
        "dashboard/services.html",
        {
            "services": services,
        },
    )


@login_required
@barbershop_required
@permission_required("can_manage_services")
def service_create(request):
    if request.method == "POST":
        form = ServiceForm(
            request.POST
        )

        if form.is_valid():
            service = form.save(
                commit=False
            )

            service.barbershop = (
                request.barbershop
            )

            service.save()

            messages.success(
                request,
                "Serviço criado com sucesso.",
            )

            return redirect(
                "dashboard:services"
            )

    else:
        form = ServiceForm()

    return render(
        request,
        "dashboard/service_form.html",
        {
            "form": form,
            "title": "Novo serviço",
            "button_text": "Criar serviço",
        },
    )


@login_required
@barbershop_required
@permission_required("can_manage_services")
def service_update(request, pk):
    service = get_object_or_404(
        Service,
        pk=pk,
        barbershop=request.barbershop,
    )

    if request.method == "POST":
        form = ServiceForm(
            request.POST,
            instance=service,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Serviço atualizado com sucesso.",
            )

            return redirect(
                "dashboard:services"
            )

    else:
        form = ServiceForm(
            instance=service
        )

    return render(
        request,
        "dashboard/service_form.html",
        {
            "form": form,
            "service": service,
            "title": "Editar serviço",
            "button_text": "Salvar alterações",
        },
    )


@login_required
@barbershop_required
@permission_required("can_manage_services")
def service_delete(request, pk):
    service = get_object_or_404(
        Service,
        pk=pk,
        barbershop=request.barbershop,
    )

    if request.method == "POST":
        name = service.name

        service.delete()

        messages.success(
            request,
            f'Serviço "{name}" excluído.',
        )

        return redirect(
            "dashboard:services"
        )

    return render(
        request,
        "dashboard/service_delete.html",
        {
            "service": service,
        },
    )


# =========================================================
# PROFISSIONAIS
# =========================================================

@login_required
@barbershop_required
def professionals(request):
    professionals = (
        Professional.objects
        .filter(
            barbershop=request.barbershop
        )
        .prefetch_related("services")
        .order_by("name")
    )

    return render(
        request,
        "dashboard/professionals.html",
        {
            "professionals": professionals,
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def professional_create(request):
    if request.method == "POST":
        form = ProfessionalForm(
            request.POST,
            request.FILES,
            barbershop=request.barbershop,
        )

        if form.is_valid():
            professional = form.save(
                commit=False
            )

            professional.barbershop = (
                request.barbershop
            )

            professional.save()

            form.save_m2m()

            messages.success(
                request,
                "Profissional criado com sucesso.",
            )

            return redirect(
                "dashboard:professionals"
            )

    else:
        form = ProfessionalForm(
            barbershop=request.barbershop
        )

    return render(
        request,
        "dashboard/professional_form.html",
        {
            "form": form,
            "title": "Novo profissional",
            "button_text": "Criar profissional",
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def professional_update(request, pk):
    professional = get_object_or_404(
        Professional,
        pk=pk,
        barbershop=request.barbershop,
    )

    if request.method == "POST":
        form = ProfessionalForm(
            request.POST,
            request.FILES,
            instance=professional,
            barbershop=request.barbershop,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profissional atualizado com sucesso.",
            )

            return redirect(
                "dashboard:professionals"
            )

    else:
        form = ProfessionalForm(
            instance=professional,
            barbershop=request.barbershop,
        )

    return render(
        request,
        "dashboard/professional_form.html",
        {
            "form": form,
            "professional": professional,
            "title": "Editar profissional",
            "button_text": "Salvar alterações",
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def professional_delete(request, pk):
    professional = get_object_or_404(
        Professional,
        pk=pk,
        barbershop=request.barbershop,
    )

    if request.method == "POST":
        name = professional.name
        professional.delete()

        messages.success(
            request,
            f'Profissional "{name}" excluído.',
        )

        return redirect(
            "dashboard:professionals"
        )

    return render(
        request,
        "dashboard/professional_delete.html",
        {
            "professional": professional,
        },
    )


# =========================================================
# HORÁRIOS
# =========================================================

@login_required
@barbershop_required
def schedules(request):
    schedules = (
        WorkSchedule.objects
        .filter(
            professional__barbershop=request.barbershop
        )
        .select_related("professional")
        .order_by(
            "professional__name",
            "weekday",
            "start_time",
        )
    )

    return render(
        request,
        "dashboard/schedules.html",
        {
            "schedules": schedules,
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def schedule_create(request):
    form = WorkScheduleForm(
        request.POST or None,
        barbershop=request.barbershop,
    )

    if (
        request.method == "POST"
        and form.is_valid()
    ):
        form.save()

        messages.success(
            request,
            "Horário criado com sucesso.",
        )

        return redirect(
            "dashboard:schedules"
        )

    return render(
        request,
        "dashboard/schedule_form.html",
        {
            "form": form,
            "title": "Novo horário",
            "button_text": "Criar horário",
        },
    )


# =========================================================
# BLOQUEIOS
# =========================================================

@login_required
@barbershop_required
def blocks(request):
    blocks = (
        ScheduleBlock.objects
        .filter(
            professional__barbershop=request.barbershop
        )
        .select_related("professional")
        .order_by(
            "-date",
            "start_time",
        )
    )

    return render(
        request,
        "dashboard/blocks.html",
        {
            "blocks": blocks,
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def block_create(request):
    form = ScheduleBlockForm(
        request.POST or None,
        barbershop=request.barbershop,
    )

    if (
        request.method == "POST"
        and form.is_valid()
    ):
        form.save()

        messages.success(
            request,
            "Bloqueio criado com sucesso.",
        )

        return redirect(
            "dashboard:blocks"
        )

    return render(
        request,
        "dashboard/block_form.html",
        {
            "form": form,
            "title": "Novo bloqueio",
            "button_text": "Criar bloqueio",
        },
    )

@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def block_update(request, pk):
    block = get_object_or_404(
        ScheduleBlock,
        pk=pk,
        professional__barbershop=request.barbershop,
    )

    form = ScheduleBlockForm(
        request.POST or None,
        instance=block,
        barbershop=request.barbershop,
    )

    if (
        request.method == "POST"
        and form.is_valid()
    ):
        form.save()

        messages.success(
            request,
            "Bloqueio atualizado com sucesso.",
        )

        return redirect(
            "dashboard:blocks"
        )

    return render(
        request,
        "dashboard/block_form.html",
        {
            "form": form,
            "block": block,
            "title": "Editar bloqueio",
            "button_text": "Salvar alterações",
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def block_delete(request, pk):
    block = get_object_or_404(
        ScheduleBlock,
        pk=pk,
        professional__barbershop=request.barbershop,
    )

    if request.method == "POST":
        block.delete()

        messages.success(
            request,
            "Bloqueio excluído com sucesso.",
        )

        return redirect(
            "dashboard:blocks"
        )

    return render(
        request,
        "dashboard/block_delete.html",
        {
            "block": block,
        },
    )


# =========================================================
# EQUIPE
# =========================================================

@login_required
@barbershop_required
@permission_required(
    "can_manage_barbershop"
)
def team(request):
    memberships = (
        Membership.objects
        .filter(
            barbershop=request.barbershop
        )
        .select_related("user")
        .order_by(
            "user__first_name",
            "user__username",
        )
    )

    return render(
        request,
        "dashboard/team.html",
        {
            "memberships": memberships,
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_barbershop"
)
def team_create(request):
    form = TeamMemberForm(
        request.POST or None
    )

    if (
        request.method == "POST"
        and form.is_valid()
    ):
        user = User.objects.create_user(
            username=form.cleaned_data[
                "username"
            ],
            first_name=form.cleaned_data[
                "first_name"
            ],
            email=form.cleaned_data[
                "email"
            ],
            password=form.cleaned_data[
                "password"
            ],
        )

        Membership.objects.create(
            user=user,
            barbershop=request.barbershop,
            role=form.cleaned_data["role"],
        )

        messages.success(
            request,
            "Membro adicionado com sucesso.",
        )

        return redirect(
            "dashboard:team"
        )

    return render(
        request,
        "dashboard/team_form.html",
        {
            "form": form,
        },
    )

@login_required
@barbershop_required
@permission_required(
    "can_manage_barbershop"
)
def team_update(request, pk):

    membership = get_object_or_404(
        Membership.objects.select_related("user"),
        pk=pk,
        barbershop=request.barbershop,
    )

    if request.method == "POST":

        role = request.POST.get("role")
        active = request.POST.get("active") == "on"

        valid_roles = {
            value
            for value, label
            in Membership.ROLE_CHOICES
        }

        if role not in valid_roles:
            messages.error(
                request,
                "Perfil inválido.",
            )

            return redirect(
                "dashboard:team_update",
                pk=membership.pk,
            )

        # Evita gerente alterando proprietário
        if (
            request.membership.role == "manager"
            and membership.role == "owner"
        ):
            messages.error(
                request,
                "Gerentes não podem alterar proprietários.",
            )

            return redirect(
                "dashboard:team"
            )

        membership.role = role
        membership.active = active
        membership.save()

        messages.success(
            request,
            "Membro atualizado com sucesso.",
        )

        return redirect(
            "dashboard:team"
        )

    return render(
        request,
        "dashboard/team_update.html",
        {
            "membership": membership,
            "role_choices": Membership.ROLE_CHOICES,
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_barbershop"
)
def team_delete(request, pk):

    membership = get_object_or_404(
        Membership.objects.select_related("user"),
        pk=pk,
        barbershop=request.barbershop,
    )

    # Não permite remover o próprio acesso
    if membership.user_id == request.user.id:
        messages.error(
            request,
            "Você não pode remover seu próprio acesso.",
        )

        return redirect(
            "dashboard:team"
        )

    # Proteção extra
    if (
        request.membership.role == "manager"
        and membership.role == "owner"
    ):
        messages.error(
            request,
            "Gerentes não podem remover proprietários.",
        )

        return redirect(
            "dashboard:team"
        )

    if request.method == "POST":

        membership.active = False
        membership.save()

        messages.success(
            request,
            "Membro removido da equipe.",
        )

        return redirect(
            "dashboard:team"
        )

    return render(
        request,
        "dashboard/team_delete.html",
        {
            "membership": membership,
        },
    )

# =========================================================
# RELATÓRIOS
# =========================================================

@login_required
@barbershop_required
def reports(request):
    return render(
        request,
        "dashboard/reports.html",
    )

@login_required
@barbershop_required
def reports(request):

    barbershop = request.barbershop

    bookings = Booking.objects.filter(
        barbershop=barbershop
    )

    completed = bookings.filter(
        status="completed"
    )

    total_bookings = (
        bookings.count()
    )

    completed_count = (
        completed.count()
    )

    cancelled_count = (
        bookings
        .filter(
            status="cancelled"
        )
        .count()
    )

    total_revenue = (
        completed
        .aggregate(
            total=Sum(
                "service__price"
            )
        )
        .get("total")
        or 0
    )

    total_customers = (
        Customer.objects
        .filter(
            barbershop=barbershop
        )
        .count()
    )

    total_professionals = (
        Professional.objects
        .filter(
            barbershop=barbershop,
            active=True,
        )
        .count()
    )

    total_services = (
        Service.objects
        .filter(
            barbershop=barbershop,
            active=True,
        )
        .count()
    )

    return render(
        request,
        "dashboard/reports.html",
        {
            "total_bookings":
                total_bookings,

            "completed_count":
                completed_count,

            "cancelled_count":
                cancelled_count,

            "total_revenue":
                total_revenue,

            "total_customers":
                total_customers,

            "total_professionals":
                total_professionals,

            "total_services":
                total_services,
        },
    )

# =========================================================
# MINHA BARBEARIA
# =========================================================

@login_required
@barbershop_required
@permission_required(
    "can_manage_barbershop"
)
def barbershop_settings(request):
    return render(
        request,
        "dashboard/barbershop_settings.html",
        {
            "barbershop": request.barbershop,
        },
    )



@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def schedule_update(request, pk):

    schedule = get_object_or_404(
        WorkSchedule,
        pk=pk,
        professional__barbershop=request.barbershop,
    )

    form = WorkScheduleForm(
        request.POST or None,
        instance=schedule,
        barbershop=request.barbershop,
    )

    if (
        request.method == "POST"
        and form.is_valid()
    ):
        form.save()

        messages.success(
            request,
            "Horário atualizado com sucesso.",
        )

        return redirect(
            "dashboard:schedules"
        )

    return render(
        request,
        "dashboard/schedule_form.html",
        {
            "form": form,
            "schedule": schedule,
            "title": "Editar horário",
            "button_text": "Salvar alterações",
        },
    )


@login_required
@barbershop_required
@permission_required(
    "can_manage_professionals"
)
def schedule_delete(request, pk):

    schedule = get_object_or_404(
        WorkSchedule,
        pk=pk,
        professional__barbershop=request.barbershop,
    )

    if request.method == "POST":

        schedule.delete()

        messages.success(
            request,
            "Horário excluído com sucesso.",
        )

        return redirect(
            "dashboard:schedules"
        )

    return render(
        request,
        "dashboard/schedule_delete.html",
        {
            "schedule": schedule,
        },
    )


from apps.subscriptions.models import Plan


@login_required
@barbershop_required
@permission_required(
    "can_manage_subscription"
)
def subscription_page(request):

    subscription = getattr(
        request.barbershop,
        "subscription",
        None,
    )

    plans = (
        Plan.objects
        .filter(active=True)
        .order_by("price")
    )

    return render(
        request,
        "dashboard/subscription.html",
        {
            "subscription": subscription,
            "plans": plans,
        },
    )

@login_required
@barbershop_required
@permission_required(
    "can_manage_subscription"
)
def subscription_upgrade(
    request,
    plan_id,
):
    plan = get_object_or_404(
        Plan,
        pk=plan_id,
        active=True,
    )

    subscription = getattr(
        request.barbershop,
        "subscription",
        None,
    )

    if not subscription:
        messages.error(
            request,
            "Sua barbearia não possui assinatura.",
        )

        return redirect(
            "dashboard:subscription"
        )

    if request.method == "POST":
        subscription.plan = plan

        # Enquanto não há gateway real:
        subscription.status = "active"

        subscription.save(
            update_fields=[
                "plan",
                "status",
                "updated_at",
            ]
        )

        messages.success(
            request,
            f"Plano alterado para {plan.name}.",
        )

    return redirect(
        "dashboard:subscription"
    )

@login_required
@barbershop_required
def settings_view(request):

    return render(
        request,
        "dashboard/settings.html",
        {
            "barbershop": request.barbershop,
            "membership": request.membership,
        },
    )

@login_required
@barbershop_required
def customers(request):

    customers = (
        Customer.objects
        .filter(
            barbershop=request.barbershop
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "dashboard/customers.html",
        {
            "customers": customers,
        },
    )

@login_required
@barbershop_required
def crm(request):
    customers = (
        Customer.objects
        .filter(
            barbershop=request.barbershop
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "dashboard/crm.html",
        {
            "customers": customers,
            "total_customers": customers.count(),
        },
    )