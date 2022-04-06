import decimal

from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, \
    HTTP_202_ACCEPTED
from rest_framework.views import APIView

from bank.api.v1.serializers import BancoSerializer, ContaSerializer, ValorSerializer, \
    ContaTransferenciaSerializer, BancoDetailSerializer, AgenciaListSerializer, AgenciaDetailsSerializer
from bank.models import Banco, Conta, Agencia
from bank.services import ContaService


class BancoListView(generics.ListCreateAPIView):
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer


class BancoDetailView(APIView):

    def get(self, request, banco_numero):
        banco = Banco.objects.filter(numero__exact=banco_numero)
        if len(banco) > 0:
            banco = banco[0]
            serializer = BancoDetailSerializer(banco)
            return Response(data=serializer.data, status=HTTP_200_OK)
        else:
            return Response(data={"msg": "banco não encontrado"}, status=HTTP_404_NOT_FOUND)


class AgenciaListView(generics.ListCreateAPIView):
    serializer_class = AgenciaListSerializer

    def get_queryset(self):
        banco_numero = self.kwargs.get("banco_numero", None)
        queryset = Agencia.objects.filter(banco__numero=banco_numero)
        return queryset

    def get_serializer_context(self):
        banco_numero = self.kwargs.get("banco_numero", None)
        return {"banco_numero": banco_numero}


class AgenciaDetailsView(APIView):

    def get(self, request, banco_numero, agencia_numero):
        agencia = Agencia.objects.filter(banco__numero__exact=banco_numero, numero=agencia_numero)
        if len(agencia) > 0:
            agencia = agencia[0]
            serializer = AgenciaDetailsSerializer(agencia)
            return Response(data=serializer.data, status=HTTP_200_OK)
        else:
            return Response(data={"msg": "agencia não encontrada"}, status=HTTP_404_NOT_FOUND)


class ContaView(APIView):
    serializer_class = ContaSerializer

    def get(self, request, banco_numero, agencia_numero):
        agencia = Agencia.objects.filter(banco__numero__exact=banco_numero, numero__exact=agencia_numero)
        if len(agencia) > 0:
            agencia = agencia[0]
            contas = Conta.objects.filter(agencia=agencia)
            serializer = ContaSerializer(contas, many=True)
            return Response(data=serializer.data, status=HTTP_200_OK)
        return Response(data={"msg": "banco ou agencia não encontrados"}, status=HTTP_404_NOT_FOUND)

    def post(self, request, banco_numero, agencia_numero):
        serializer = ContaSerializer(data=request.data,
                                     context={"banco_numero": banco_numero, "agencia_numero": agencia_numero})
        if serializer.is_valid():
            serializer.save()
            return Response(data={"data": serializer.data}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ContaSaqueView(APIView):
    serializer_class = ValorSerializer

    def post(self, request, banco_numero, agencia_numero, conta_numero):
        valor_a_sacar = decimal.Decimal(request.data['valor'])
        conta = ContaService.sacar(banco_numero, agencia_numero, conta_numero, valor_saque=valor_a_sacar)
        serializer = ContaSerializer(conta)
        return Response(serializer.data, status=HTTP_202_ACCEPTED)


class ContaDepositoView(APIView):
    serializer_class = ValorSerializer

    def post(self, request, banco_numero, agencia_numero, conta_numero):
        valor_a_depositar = decimal.Decimal(request.data['valor'])
        conta = ContaService.depositar(banco_numero, agencia_numero, conta_numero, valor_a_depositar=valor_a_depositar)
        serializer = ContaSerializer(conta)
        return Response(serializer.data)


class ContaTransferenciaView(APIView):
    serializer_class = ContaTransferenciaSerializer

    @transaction.atomic()
    def post(self, request, banco_numero, agencia_numero, conta_numero):
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
