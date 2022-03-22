from django.contrib import admin

# Register your models here.
from bank.models import Banco, Conta, Agencia, Titular

admin.site.register(Banco)
admin.site.register(Conta)
admin.site.register(Agencia)
admin.site.register(Titular)