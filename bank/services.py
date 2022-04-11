from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from bank.models import Conta


class ContaService(object):

    @staticmethod
    def get_obj(banco_numero, agencia_numero, conta_numero):
        conta = get_object_or_404(Conta,
                                  agencia__banco__numero=banco_numero,
                                  agencia__numero=agencia_numero,
                                  numero=conta_numero)
        return conta

    @staticmethod
    def sacar(banco_numero=None, agencia_numero=None, conta_numero=None, valor_saque=0.0, instance=None):
        conta = None
        if instance:
            conta = instance
        else:
            conta = ContaService.get_obj(banco_numero=banco_numero,
                                         agencia_numero=agencia_numero,
                                         conta_numero=conta_numero)
        if conta.saldo - valor_saque >= 0.0:
            conta.saldo -= valor_saque
            conta.save()
            return conta

        raise ValidationError({"status": "Recusado: Saldo insuficiente"})

    @staticmethod
    def depositar(banco_numero=None, agencia_numero=None, conta_numero=None, valor_a_depositar=0.0, instance=None):
        conta = None
        if instance:
            conta = instance
        else:
            conta = ContaService.get_obj(banco_numero=banco_numero, agencia_numero=agencia_numero,
                                         conta_numero=conta_numero)
        conta.saldo += valor_a_depositar
        conta.save()
        return conta

    @staticmethod
    def transferir(banco_numero_origem=None, agencia_numero_origem=None, conta_numero_origem=None,
                   banco_numero_destino=None, agencia_numero_destino=None, conta_numero_destino=None,
                   valor_a_transferir=0.0, instance=None):

        ContaService.sacar(banco_numero=banco_numero_origem, agencia_numero=agencia_numero_origem,
                           conta_numero=conta_numero_origem, valor_saque=valor_a_transferir)

        ContaService.depositar(banco_numero=banco_numero_destino, agencia_numero=agencia_numero_destino,
                               conta_numero=conta_numero_destino, valor_a_depositar=valor_a_transferir)

        return True
