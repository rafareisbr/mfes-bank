from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from bank.models import Banco, Conta, Agencia, Titular


class BancoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banco
        fields = ('numero', 'nome')


class AgenciaListSerializer(serializers.ModelSerializer):
    banco = serializers.CharField(source="banco.nome", read_only=True)
    contas_registradas = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Agencia
        fields = ('numero', 'banco', 'contas_registradas')

    def get_contas_registradas(self, obj):
        return obj.contas.count()

    def create(self, validated_data):
        conta_numero = validated_data.get('numero')
        banco_numero = self.context["banco_numero"]

        banco = get_object_or_404(Banco, numero=banco_numero)

        agencia = Agencia.objects.create(numero=conta_numero, banco=banco)
        return agencia


class BancoDetailSerializer(serializers.ModelSerializer):
    agencias = AgenciaListSerializer(many=True)

    class Meta:
        model = Banco
        fields = ("numero", "nome", "agencias")


class TitularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titular
        fields = "__all__"


class ContaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conta
        fields = ('numero', 'saldo')


class ContaSerializer(serializers.ModelSerializer):
    titular = TitularSerializer()
    banco_numero = serializers.CharField(source="agencia.banco.numero", read_only=True)
    agencia_numero = serializers.CharField(source="agencia.numero", read_only=True)

    class Meta:
        model = Conta
        fields = ('numero', 'saldo', 'titular', 'banco_numero', 'agencia_numero')

    @transaction.atomic
    def create(self, validated_data):
        banco_numero = self.context['banco_numero']
        agencia_numero = self.context['agencia_numero']
        agencia = Agencia.objects.get(banco__numero__exact=banco_numero, numero__exact=agencia_numero)

        # create titular
        titular_data = validated_data.pop('titular')
        titular, created = Titular.objects.get_or_create(cpf=titular_data["cpf"], nome=titular_data["nome"])

        if created:
            print("novo usuário")

        conta = Conta(agencia=agencia, titular=titular, **validated_data)
        conta.save()

        return conta


class AgenciaDetailsSerializer(serializers.ModelSerializer):
    contas = ContaListSerializer(many=True)
    banco = BancoSerializer()

    class Meta:
        model = Agencia
        fields = ('numero', 'banco', 'contas')


class ValorSerializer(serializers.Serializer):
    valor = serializers.DecimalField(max_digits=12, decimal_places=2, required=True, min_value=0.01)


class ContaTransferenciaSerializer(serializers.Serializer):
    banco_numero_destino = serializers.CharField(max_length=50)
    agencia_numero_destino = serializers.CharField(max_length=50)
    conta_numero_destino = serializers.CharField(max_length=50)
    valor_a_transferir = serializers.DecimalField(max_digits=12, decimal_places=2, required=True, min_value=0.01)
