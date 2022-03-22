from django.shortcuts import get_object_or_404

from bank.models import Conta


class ContaService(object):

    @staticmethod
    def get_obj(banco_numero, agencia_numero, conta_numero):
        conta = get_object_or_404(Conta, agencia__banco__numero=banco_numero, agencia__numero=agencia_numero,
                                  numero=conta_numero)
        return conta

    @staticmethod
    def sacar(banco_numero, agencia_numero, conta_numero, valor_saque):
        conta = ContaService.get_obj(banco_numero=banco_numero, agencia_numero=agencia_numero,
                                     conta_numero=conta_numero)
        if conta.saldo - valor_saque >= 0.0:
            conta.saldo -= valor_saque
            conta.save()
            return conta
        raise Exception("recusado - saldo insuficiente")

    @staticmethod
    def depositar(banco_numero, agencia_numero, conta_numero, valor_a_depositar):
        conta = ContaService.get_obj(banco_numero=banco_numero, agencia_numero=agencia_numero,
                                     conta_numero=conta_numero)
        conta.saldo += valor_a_depositar
        conta.save()
        return conta

    @staticmethod
    def transferir(banco_numero_origem, agencia_numero_origem, conta_numero_origem,
                   banco_numero_destino, agencia_numero_destino, conta_numero_destino,
                   valor_a_transferir):

        ContaService.sacar(banco_numero=banco_numero_origem, agencia_numero=agencia_numero_origem,
                           conta_numero=conta_numero_origem, valor_saque=valor_a_transferir)

        ContaService.depositar(banco_numero=banco_numero_destino, agencia_numero=agencia_numero_destino,
                               conta_numero=conta_numero_destino, valor_a_depositar=valor_a_transferir)

        return True
