from django.urls import path, include
from rest_framework_nested import routers

from bank.api.v2.views import BancoViewSet, AgenciaViewSet, ContaViewSet

router = routers.DefaultRouter()
router.register("bancos", BancoViewSet, basename='bancos')

banco_router = routers.NestedSimpleRouter(router, "bancos", lookup="banco")
banco_router.register("agencias", AgenciaViewSet, basename="agencias")

agencia_router = routers.NestedSimpleRouter(banco_router, "agencias", lookup="agencia")

agencia_router.register("contas", ContaViewSet, basename="contas")

urlpatterns = [
    path("", include(router.urls),),
    path("", include(banco_router.urls)),
    path("", include(agencia_router.urls))
]