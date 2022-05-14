from django.forms import ModelForm
from .models import *
from django.urls import reverse_lazy

#Para preenchimento da lista de portas da cto
PORTAS_CHOICES=(
    ('4','4'),
    ('8','8'),
    ('16','16'),
    ('32','32')
)

#Para preenchimento da lista de portas da onu
#QTDPORTAS-ONU_CHOICES=(
#    ('1','1'),
#    ('2','2'),
#    ('3','3'),
#    ('4','4'),
#    ('5','5')
#)

#Para preenchimento da lista de portas da onu
#SINAL-CTO_CHOICES=(
#    ('1','1'),
#    ('2','2'),
#    ('3','3'),
#    ('4','4'),
#    ('5','5')
#)


class ProvisionarForm(ModelForm):
    class Meta:
        model = Provisionado
        fields = "__all__"
        #fields = ['user', 'cto', 'portaCto', 'modo','vlan', 'onu', 'sinal', 'dataInstalacao']

class UserForm(ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        #fields = ['nomeCliente', 'nomeUser', 'password', 'latitude','longitude', 'descricao', 'plano']

class PlanoForm(ModelForm):
    class Meta:
        model = Plano
        fields = "__all__"
        #fields = ['nomePlano', 'down', 'up']

class  FabricanteForm(ModelForm):
    class Meta:
        model = Fabricante
        fields = ['nomeFabricante', 'descricao']

class  ModeloOltForm(ModelForm):
    class Meta:
        model =ModeloOlt
        fields = ['fabricante', 'nomeModeloOlt', 'quantPortas','descricao']

class  ModeloOnuForm(ModelForm):
    class Meta:
        model =ModeloOnu
        fields = ['fabricante', 'nomeModeloOnu', 'quantPortasLans', 'wifi','descricao']

class  OltForm(ModelForm):
    class Meta:
        model =Olt
        fields = ['modelo', 'nomeOlt', 'ip', 'login','senha']

class  PonForm(ModelForm):
    class Meta:
        model =Pon
        fields = ['olt', 'nomePon', 'sinalPon', 'portaPon']

class  ModoForm(ModelForm):
    class Meta:
        model =Modo
        fields = ['nomeModo']

class  VlanForm(ModelForm):
    class Meta:
        model =Vlan
        fields = ['modo', 'nomeValn', 'vlanID', 'pon']

class  CtoForm(ModelForm):
    class Meta:
        model =Cto
        fields = "__all__"
        #fields = ['pon','nomeCto', 'sinalCto', 'descricao', 'qtdPortas', 'latitude', 'longitude']

class  OnuForm(ModelForm):
    class Meta:
        model =Onu
        fields = ['modeloOnu', 'serial']

class  PortasCtoForm(ModelForm):
    class Meta:
        model =PortasCto
        #fields = ['cto', 'numeroPorta','statusPorta']
        fields = "__all__"
