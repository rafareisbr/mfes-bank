import decimal

from django.db import transaction
from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED

from bank.api.v1.serializers import BancoSerializer, ContaSerializer, AgenciaListSerializer, ValorSerializer, \
    ContaTransferenciaSerializer
from bank.models import Banco, Conta, Agencia
from bank.services import ContaService


class BancoViewSet(viewsets.ModelViewSet):
    serializer_class = BancoSerializer
    lookup_field = 'numero'

    def get_queryset(self, **kwargs):
        return Banco.objects.all()


class AgenciaViewSet(viewsets.ModelViewSet):
    serializer_class = AgenciaListSerializer
    lookup_field = 'numero'

    def get_queryset(self):
        banco_numero = self.kwargs["banco_numero"]
        return Agencia.objects.filter(banco__numero=banco_numero)


class ContaViewSet(viewsets.ModelViewSet):
    serializer_class = ContaSerializer
    lookup_field = 'numero'

    def get_queryset(self):
        banco_numero = self.kwargs["banco_numero"]
        agencia_numero = self.kwargs["agencia_numero"]
        return Conta.objects.filter(agencia__numero=agencia_numero, agencia__banco__numero=banco_numero)


class ContaDepositoSaqueViewSet(viewsets.GenericViewSet):
    serializer_class = ValorSerializer
    lookup_field = "numero"

    @action(detail=True, methods=['post'])
    @transaction.atomic()
    def sacar(self, request, numero=None, *args, **kwargs):
        banco_numero = self.kwargs["banco_numero"]
        agencia_numero = self.kwargs["agencia_numero"]
        conta_numero = numero

        valor_saque = decimal.Decimal(request.data['valor'])
        conta = ContaService.sacar(banco_numero=banco_numero, agencia_numero=agencia_numero, conta_numero=conta_numero,
                                   valor_saque=valor_saque)
        serializer = ContaSerializer(conta)
        return Response(serializer.data, status=HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    @transaction.atomic()
    def depositar(self, request, numero=None, *args, **kwargs):
        banco_numero = self.kwargs["banco_numero"]
        agencia_numero = self.kwargs["agencia_numero"]
        conta_numero = numero
        valor_a_depositar = decimal.Decimal(request.data['valor'])

        conta = ContaService.depositar(banco_numero=banco_numero, agencia_numero=agencia_numero, conta_numero=conta_numero,
                                       valor_a_depositar=valor_a_depositar)
        serializer = ContaSerializer(conta)
        return Response(serializer.data)


class ContaTransferenciaViewSet(viewsets.GenericViewSet):
    serializer_class = ContaTransferenciaSerializer
    lookup_field = "numero"

    @action(detail=True, methods=['post'])
    @transaction.atomic()
    def transferir(self, request, numero=None, *args, **kwargs):
        banco_numero = self.kwargs["banco_numero"]
        agencia_numero = self.kwargs["agencia_numero"]
        conta_numero = numero

        valor_a_transferir = decimal.Decimal(request.data['valor_a_transferir'])
        banco_numero_destino = request.data['banco_numero_destino']
        agencia_numero_destino = request.data['agencia_numero_destino']
        conta_numero_destino = request.data['conta_numero_destino']

        success = ContaService.transferir(
            banco_numero_origem=banco_numero, agencia_numero_origem=agencia_numero, conta_numero_origem=conta_numero,
            banco_numero_destino=banco_numero_destino, agencia_numero_destino=agencia_numero_destino,
            conta_numero_destino=conta_numero_destino, valor_a_transferir=valor_a_transferir)

        if success:
            return Response({"status": "transferencia realizado com sucesso"})