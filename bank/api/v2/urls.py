from django.urls import path
from django.views.generic import TemplateView

from bank.api.v2.views import BancoDetailView, ContaView, ContaSaqueView, AgenciaListView, ContaDepositoView, \
    ContaTransferenciaView, BancoListView, AgenciaDetailsView

urlpatterns = [
    path("bancos/", BancoListView.as_view()),

    path("bancos/<str:banco_numero>/", BancoDetailView.as_view()),

    path("bancos/<str:banco_numero>/agencias/", AgenciaListView.as_view()),

    path("bancos/<str:banco_numero>/agencias/<str:agencia_numero>/", AgenciaDetailsView.as_view()),

    path("bancos/<str:banco_numero>/agencias/<str:agencia_numero>/contas/", ContaView.as_view()),

    # Operacoes
    path(
        "bancos/<str:banco_numero>/agencias/<str:agencia_numero>/contas/<str:conta_numero>/sacar/",
        ContaSaqueView.as_view()
    ),
    path(
        "bancos/<str:banco_numero>/agencias/<str:agencia_numero>/contas/<str:conta_numero>/depositar/",
        ContaDepositoView.as_view()
    ),
    path(
        "bancos/<str:banco_numero>/agencias/<str:agencia_numero>/contas/<str:conta_numero>/transferir/",
            ContaTransferenciaView.as_view()
    ),
]
