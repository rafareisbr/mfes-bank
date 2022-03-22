from django.contrib.auth.models import User
from django.db import models


class Banco(models.Model):
    numero = models.CharField(max_length=30, blank=False)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Agencia(models.Model):
    numero = models.CharField(max_length=255, blank=False)
    banco = models.ForeignKey(to='bank.Banco', on_delete=models.CASCADE, related_name='agencias')

    def __str__(self):
        return f"{self.banco.nome} - {self.numero}"

    class Meta:
        unique_together = [['numero', 'banco']]


class Titular(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True,)

    def __str__(self):
        return f"{self.nome} {self.cpf}"


class Conta(models.Model):
    numero = models.CharField(max_length=255, blank=False)
    saldo = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    titular = models.ForeignKey(to='bank.Titular', on_delete=models.CASCADE, related_name='contas')
    agencia = models.ForeignKey(to='bank.Agencia', on_delete=models.CASCADE, related_name='contas')

    class Meta:
        unique_together = [['numero', 'agencia_id']]

    def __str__(self):
        return self.numero