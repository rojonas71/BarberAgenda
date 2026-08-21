from django.urls import path
from . import views

app_name = "dashboard"


urlpatterns = [

    # =========================
    # PRINCIPAL
    # =========================

    path(
        "",
        views.dashboard_home,
        name="home",
    ),

    path(
        "agenda/",
        views.agenda,
        name="agenda",
    ),

    path(
     "agendamentos/",
     views.booking_list,
     name="bookings",
    ),


    # =========================
    # OPERAÇÃO
    # =========================

    path(
        "servicos/",
        views.services,
        name="services",
    ),

    path(
    "servicos/novo/",
    views.service_create,
    name="service_create",
),

path(
    "servicos/<int:pk>/editar/",
    views.service_update,
    name="service_update",
),

path(
    "servicos/<int:pk>/excluir/",
    views.service_delete,
    name="service_delete",
),

    path(
        "profissionais/",
        views.professionals,
        name="professionals",
    ),
    path(
    "servicos/novo/",
    views.service_create,
    name="service_create",
),

path(
    "servicos/<int:pk>/editar/",
    views.service_update,
    name="service_update",
),

path(
    "servicos/<int:pk>/excluir/",
    views.service_delete,
    name="service_delete",
),

    path(
        "horarios/",
        views.schedules,
        name="schedules",
    ),

    path(
    "horarios/novo/",
    views.schedule_create,
    name="schedule_create",
),

path(
    "horarios/<int:pk>/editar/",
    views.schedule_update,
    name="schedule_update",
),

path(
    "horarios/<int:pk>/excluir/",
    views.schedule_delete,
    name="schedule_delete",
),

    path(
        "bloqueios/",
        views.blocks,
        name="blocks",
    ),

    path(
    "bloqueios/novo/",
    views.block_create,
    name="block_create",
),

path(
    "bloqueios/<int:pk>/editar/",
    views.block_update,
    name="block_update",
),

path(
    "bloqueios/<int:pk>/excluir/",
    views.block_delete,
    name="block_delete",
),


    # =========================
    # GESTÃO
    # =========================

    path(
        "equipe/",
        views.team,
        name="team",
    ),

    path(
    "equipe/novo/",
    views.team_create,
    name="team_create",
),

path(
    "equipe/<int:pk>/editar/",
    views.team_update,
    name="team_update",
),

path(
    "equipe/<int:pk>/remover/",
    views.team_delete,
    name="team_delete",
),

    path(
        "relatorios/",
        views.reports,
        name="reports",
    ),

    path(
        "minha-barbearia/",
        views.barbershop_settings,
        name="barbershop_settings",
    ),

    path(
    "profissionais/novo/",
    views.professional_create,
    name="professional_create",
),

path(
    "profissionais/<int:pk>/editar/",
    views.professional_update,
    name="professional_update",
),

path(
    "profissionais/<int:pk>/excluir/",
    views.professional_delete,
    name="professional_delete",
),

path(
    "plano/",
    views.subscription_page,
    name="subscription",
),

path(
    "plano/<int:plan_id>/upgrade/",
    views.subscription_upgrade,
    name="subscription_upgrade",
),

path(
    "configuracoes/",
    views.settings_view,
    name="settings",
),

path(
    "clientes/",
    views.customers,
    name="customers",
),

path(
    "crm/",
    views.crm,
    name="crm",
),

]