from django.contrib import admin
from .models import *

admin.site.site_header='Sistema Experimentall'
admin.site.site_title='Projeto FTTH'
admin.site.index_title='FTTH'

# Register your models here.
@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nomePlano', 'down', 'up')

@admin.register(Cliente)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nomeCliente', 'nomeUser', 'emailUser', 'password', 'latitude', 'longitude', 'descricao', 'plano')

@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('nomeFabricante', 'descricao')

@admin.register(ModeloOlt)
class ModeloOltAdmin(admin.ModelAdmin):
    list_display = ('fabricante', 'nomeModeloOlt', 'quantPortas', 'descricao')

@admin.register(ModeloOnu)
class ModeloOnuAdmin(admin.ModelAdmin):
        list_display = ('fabricante', 'nomeModeloOnu', 'quantPortasLans', 'wifi', 'descricao')

@admin.register(Olt)
class OltAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'nomeOlt', 'ip', 'login', 'senha')

@admin.register(Pon)
class PonAdmin(admin.ModelAdmin):
    list_display = ('olt', 'nomePon', 'sinalPon', 'portaPon')

@admin.register(Vlan)
class VlanAdmin(admin.ModelAdmin):
    list_display = ('modo', 'nomeValn', 'vlanID', 'pon')

@admin.register(Cto)
class CtoAdmin(admin.ModelAdmin):
    list_display = ('pon', 'nomeCto', 'sinalCto', 'descricao', 'qtdPortas', 'latitude', 'longitude')

@admin.register(Onu)
class OnuAdmin(admin.ModelAdmin):
    list_display = ('modeloOnu', 'serial')

@admin.register(PortasCto)
class PortasCtoAdmin(admin.ModelAdmin):
     list_display = ('cto', 'numeroPorta', 'statusPorta', 'descricao', 'desprovisionar')

@admin.register(Provisionado)
class FtthAdmin(admin.ModelAdmin):
    list_display = ('user', 'cto', 'portaCto', 'modo', 'vlan', 'onu', 'sinal', 'dataInstalacao')

admin.site.register(Modo)