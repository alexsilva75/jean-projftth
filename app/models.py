from stdimage.models import StdImageField
import uuid
from django.db import models

#modifica o nome da foto para nao ter igual
def get_file_path(_instance, filename):
    ext=filename.split('.')[-1]
    filename=f'{uuid.uuid4()}.{ext}'
    return filename

# Para preenchimento da lista de portas da cto
PORTA_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16')
)

MODOS_CHOICES = (
    ('bridge', 'bridge'),
    ('router', 'router'),
    ('outro', 'outro'),
)

class Localizacao(models.Model):

    latitude = models.CharField('Latitude', max_length=100, null=True, blank=True, default='')
    longitude = models.CharField('Longitude', max_length=100, null=True, blank=True, default='')
    descricao = models.TextField('Descrição', null=True, blank=True, default='Escreva sua descrição aqui')
    data = models.DateField('Data de Instalação', auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract=True

#atualizado url
class Plano(models.Model):
    nomePlano = models.CharField('Plano', max_length=100)
    down = models.CharField('Down', max_length=100)
    up =models.CharField('Up', max_length=100)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return f'{self.nomePlano} - {self.down}'

#atualizado url
class Cliente(Localizacao):
    nomeCliente = models.CharField('Nome', max_length=100, null=True, blank=True)
    nomeUser = models.CharField('Usuário', max_length=100, null=True, blank=True)
    emailUser = models.EmailField('Email', null=True, blank=True, default='cliente@portalcrtelecom.com.br')
    password = models.CharField('Senha', max_length=100, null=True, blank=True, default='cr')
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.nomeUser

#atualizado url
class Fabricante(models.Model):
    nomeFabricante = models.CharField('Fabricante', max_length=100, null=True, blank=True)
    descricao = models.TextField('Descricao', null=True, blank=True)

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'

    def __str__(self):
        return self.nomeFabricante

#atualizado url
class ModeloOlt(models.Model):
    PORTA_CHOICES = (
        ('4', '4'),
        ('8', '8'),
        ('16', '16')
    )
    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, null=True)
    nomeModeloOlt = models.CharField('Modelo', max_length=100, null=True, blank=True)
    quantPortas = models.CharField('Porta Pon', max_length=100, null=True, blank=True,
                                 choices=PORTA_CHOICES)

    descricao = models.TextField('Descricao', null=True, blank=True)



    class Meta:
        verbose_name = 'ModeloOlt'
        verbose_name_plural = 'ModelosOlt'

    def __str__(self):
        return self.nomeModeloOlt

#atualizado url
class ModeloOnu(models.Model):
    SN_CHOICES = (
        ('s', 's'),
        ('n', 'n')
    )

    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, null=True)
    nomeModeloOnu = models.CharField('Modelo', max_length=100, null=True, blank=True)
    quantPortasLans = models.CharField('Quantidade de portas', max_length=100, null=True, blank=True, default='1')
    wifi = models.CharField('Tem wifi?', max_length=100, null=True, blank=True,
                                 choices=SN_CHOICES, default='n')
    descricao = models.TextField('Descricao', null=True, blank=True)

    class Meta:
        verbose_name = 'ModeloOnu'
        verbose_name_plural = 'ModelosOnu'

    def __str__(self):
        return self.nomeModeloOnu

#atualizado url
class Olt(Localizacao):
    modelo = models.ForeignKey(ModeloOlt, on_delete=models.SET_NULL, null=True)
    nomeOlt = models.CharField('Apelido da Olt', max_length=100, null=True, blank=True)
    ip = models.CharField('Endereço IP', max_length=100, null=True, blank=True)
    login = models.CharField('Login', max_length=100, null=True, blank=True, default='admin')
    senha = models.CharField('Senha', max_length=100, null=True, blank=True, default='parks')
#    imagem = StdImageField('Imagem', upload_to='get_file_path', variations={'thumb':{'width':480,'height':400, 'crop':True}})

    class Meta:
        verbose_name = 'Olt'
        verbose_name_plural = 'OLTs'

    def __str__(self):
        return self.nomeOlt

#atualizado url
class Pon(models.Model):
    olt = models.ForeignKey(Olt, on_delete=models.SET_NULL, null=True)
    nomePon = models.CharField('Pon/Área', max_length=100, null=True, blank=True)
    sinalPon = models.CharField('Sinal em dBm', max_length=100, null=True, blank=True)
    portaPon = models.CharField('Porta Pon', max_length=100, null=True, blank=True,
                                 choices=PORTA_CHOICES)

    class Meta:
        verbose_name = 'PON'
        verbose_name_plural = 'PONs'

    def __str__(self):
        return self.nomePon

#atualizado url
class Modo(models.Model):

    nomeModo = models.CharField('Modo', max_length=100, null=True, blank=True, choices=MODOS_CHOICES)

    class Meta:
        verbose_name = 'Modo'
        verbose_name_plural = 'Modos'

    def __str__(self):
        return self.nomeModo

#atualizado url
class Vlan(models.Model):
    modo = models.ForeignKey(Modo, on_delete=models.SET_NULL, blank=True, null=True)
    nomeValn = models.CharField('Vlan', max_length=100, null=True, blank=True)
    vlanID = models.CharField('ID da Vlan', max_length=100, null=True, blank=True)
    pon = models.ForeignKey(Pon, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'VLAN'
        verbose_name_plural = 'VLANs'

    def __str__(self):
        return self.nomeValn

#atualizado url
class Cto(Localizacao):
    PORTAS_OLT_CHOICES = (
        ('8', '8'),
        ('16', '16'),
        ('128', '128')
    )

    qtdPortas = models.CharField('Quantidade de Portas', max_length=100, null=True, blank=True, choices=PORTAS_OLT_CHOICES, default='8')
    pon = models.ForeignKey(Pon, on_delete=models.SET_NULL, null=True)
    nomeCto = models.CharField('Nome da CTO', max_length=100, unique=True, null=True, blank=True)
    sinalCto = models.CharField('Sinal da CTO', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'CTO'
        verbose_name_plural = 'CTOs'

    def __str__(self):
        return self.nomeCto

#atualizado url
class Onu(models.Model):
    modeloOnu = models.ForeignKey(ModeloOnu, on_delete=models.SET_NULL, null=True)
    serial = models.CharField('Número do Serial', max_length=100, null=True, blank=True, unique=True)#unique=True não aceita repeticoes

    class Meta:
        verbose_name = 'ONU'
        verbose_name_plural = 'ONUs'

    def __str__(self):
        return self.serial

#atualizado url
class PortasCto(models.Model):

    STATUS_PORTAS_CHOICES = (
        ('ocupada', 'ocupada'),
        ('livre', 'livre')
    )

    cto = models.ForeignKey(Cto, on_delete=models.SET_NULL, null=True)
    #numeroPorta = models.CharField('Número da Porta', max_length=100, null=True, blank=True, choices=PORTA_CHOICES)
    numeroPorta = models.CharField(max_length=100, unique=False)
    statusPorta = models.CharField('Status Da Porta', max_length=100, null=True, blank=True, choices=STATUS_PORTAS_CHOICES, default='livre')
    descricao = models.TextField('Descrição', null=True, blank=True)
    desprovisionar=models.TextField('Desprovisionar', null=True, blank=True)
    class Meta:
        verbose_name = 'Porta'
        verbose_name_plural = 'Portas'

    def __str__(self):
       # return f'{self.numeroPorta} - {self.statusPorta}'
        return self.numeroPorta


class Provisionado(models.Model):

    #user = models.OneToOneField(Cliente, on_delete=models.SET_NULL, null=True)
    user = models.CharField(max_length=100, null=True, unique=True, blank=True)
    olt = models.ForeignKey(Olt, on_delete=models.SET_NULL, null=True)
    pon = models.ForeignKey(Pon, on_delete=models.SET_NULL, null=True)
    cto = models.ForeignKey(Cto, on_delete=models.SET_NULL, null=True)
    portaCto = models.OneToOneField(PortasCto, on_delete=models.SET_NULL, null=True)
    onu = models.CharField(max_length=100, null=True, unique=True, blank=True)
    modo = models.CharField('Modo', max_length=100, null=True, blank=True, choices=MODOS_CHOICES, default='bridge')
    vlan = models.ForeignKey(Vlan, on_delete=models.SET_NULL, null=True)
    #onu = models.OneToOneField(Onu, on_delete=models.SET_NULL, null=True)
    sinal = models.CharField(max_length=100, null=True, blank=True)
    dataInstalacao = models.DateTimeField('Data da Instalação', null=True, blank=True, auto_now_add=True)
    #dataInstalacao = models.DateTimeField('Data da Instalação', null=True, blank=True)

    class Meta:
        verbose_name = 'Provisionamento'
        verbose_name_plural = 'Provisionamentos'

    def __str__(self):
        return "provisionamento"