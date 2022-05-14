from paramiko import SSHClient
import paramiko

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages

from .form import *
from .models import *


def ssh_connect(cmd):
    clientssh = SSHClient()
    clientssh.load_system_host_keys()
    clientssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        clientssh.connect(hostname='187.87.200.54', username='pdncrtel', password='pdncrtl@2021', port='1883')
        session = clientssh.get_transport().open_session()
    except Exception as err:
        print("Erro de login: " + str(err))

    if session.active:
        print(session.exec_command(''))
        print('aqui')
        result = session.recv(1024)
        clientssh.get_transport().close()
        print(result)
    return


class IndexView(TemplateView):
    template_name = 'index.html'


class ProvisionadosView(TemplateView):
    template_name = 'listaProvisionados.html'

    def get_context_data(self, **kwargs):
        context = super(ProvisionadosView, self).get_context_data(**kwargs)
        context['objetos'] = Provisionado.objects.order_by('cto').all()
        return context


def listaProvisionadosOrder(request, pk):
    if pk == '1':
        campo = 'dataInstalacao'
    elif pk == '2':
        campo = 'user'
    elif pk == '3':
        campo = 'onu'
    else:
        campo = 'id'

    objetos_list = Provisionado.objects.order_by(campo).all()
    paginator = Paginator(objetos_list, 10)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    objetos = paginator.get_page(page_number)
    return render(request, 'listaProvisionados.html', {'objetos': objetos})


def listaProvisionados(request):
    objetos_list = Provisionado.objects.order_by('id').all().reverse()
    paginator = Paginator(objetos_list, 10)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    objetos = paginator.get_page(page_number)
    # ssh_connect('com')
    return render(request, 'listaProvisionados.html', {'objetos': objetos})


# def home(request):
#    return render(request,'olt/home.html')
#

def novo_provisionamento(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = ProvisionarForm(request.POST or None)
        if form.is_valid():

            dados = form.save(commit=False)
            form.save()
            # print(f'status da porta = {dados.portaCto.id}')
            pk = dados.portaCto.id
            portaCto = PortasCto.objects.get(pk=pk)

            portaCto.statusPorta = 'ocupada'
            if dados.modo == 'bridge':
                portaCto.descricao = f'configure terminal\ninterface gpon1/{dados.vlan.pon.portaPon}\nonu add serial-number {dados.onu}\nonu {dados.onu} alias {dados.user}\nonu {dados.onu} flow-profile bridge_vlan_{dados.vlan.vlanID}_pon{dados.vlan.pon.portaPon}\nonu {dados.onu} vlan-translation _{dados.vlan.vlanID} uni-port 1\nend\ncopy r s \n'
            elif dados.modo == 'router':
                portaCto.descricao = f'configure terminal\ninterface gpon1/{dados.portaCto.cto.pon.portaPon}\nonu add serial-number {dados.onu}\nonu {dados.onu} alias {dados.user}\nonu {dados.onu} flow-profile router_vlan_{dados.vlan.vlanID}\nend\ncopy r s\n'
            portaCto.desprovisionar = f'configure terminal\ninterface gpon1/{dados.portaCto.cto.pon.portaPon}\nno onu {dados.onu}\nend\ncopy r s\n'
            portaCto.save()
            # provisionar = Provisionado.objects.get(pk=pk)
            # return redirect('url_listaProvisionados')
            return redirect('url_nova_provisionamento')

        data['form'] = form
        return render(request, 'formProvisionamento.html', data)


def update_provisionamento(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        provisionar = Provisionado.objects.get(pk=pk)
        form = ProvisionarForm(request.POST or None, instance=provisionar)
        if form.is_valid():
            ##################
            dados = form.save(commit=False)
            form.save()
            # print(f'status da porta = {dados.portaCto.id}')
            pk = dados.portaCto.id
            portaCto = PortasCto.objects.get(pk=pk)
            portaCto.statusPorta = 'ocupada'
            portaCto.save()
            ###################
            # form.save()
            return redirect('url_listaProvisionados')
        data['form'] = form
        data['provisionar'] = provisionar
        return render(request, 'formProvisionamento.html', data)


def delete_provisionamento(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        provisionar = Provisionado.objects.get(pk=pk)
        provisionar.delete()
        return redirect('url_listaProvisionados')


# novo

class ClientesView(TemplateView):
    template_name = 'listaClientes.html'

    def get_context_data(self, **kwargs):
        context = super(ClientesView, self).get_context_data(**kwargs)
        context['objetos'] = Cliente.objects.all();
        return context


def novo_cliente(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaClientes')
        data['form'] = form
        return render(request, 'formCliente.html', data)


def update_cliente(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        cliente = Cliente.objects.get(pk=pk)
        form = UserForm(request.POST or None, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('url_listaClientes')
        data['form'] = form
        data['cliente'] = cliente
        return render(request, 'formCliente.html', data)


def delete_cliente(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        cliente = Cliente.objects.get(pk=pk)
        cliente.delete()
        return redirect('url_listaClientes')


class PlanosView(TemplateView):
    template_name = 'listaPlanos.html'

    def get_context_data(self, **kwargs):
        context = super(PlanosView, self).get_context_data(**kwargs)
        context['objetos'] = Plano.objects.all();
        return context


def novo_plano(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = PlanoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaPlanos')
        data['form'] = form
        return render(request, 'formPlano.html', data)


def update_plano(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = Plano.objects.get(pk=pk)
        form = PlanoForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaPlanos')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formPlano.html', data)


def delete_plano(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = Plano.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaPlanos')
    messages.success(request, 'Excluido com sucesso!')


# teste de aprendizagem oram eitos primeiro em fabricante

class FabricantesView(TemplateView):
    template_name = 'listaFabricantes.html'

    def get_context_data(self, **kwargs):
        context = super(FabricantesView, self).get_context_data(**kwargs)
        context['objetos'] = Fabricante.objects.all();
        return context


def novo_fabricante(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')  #
    else:
        data = {}
        form = FabricanteForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaFabricantes')  #
        data['form'] = form
        return render(request, 'formFabricante.html', data)  #


def update_fabricante(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_home')
    else:
        data = {}
        # objeto = Fabricante.objects.get(pk=pk)
        objeto = get_object_or_404(Fabricante, pk=pk)
        form = FabricanteForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaFabricantes')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formFabricante.html', data)


def delete_fabricante(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        # objeto = Fabricante.objects.get(pk=pk)
        objeto = get_object_or_404(Fabricante, pk=pk)
        objeto.delete()
        return redirect('url_listaFabricantes')


class ModeloOltsView(TemplateView):
    template_name = 'listaModeloOlts.html'

    def get_context_data(self, **kwargs):
        context = super(ModeloOltsView, self).get_context_data(**kwargs)
        context['objetos'] = ModeloOlt.objects.all();
        return context


def novo_modeloOlt(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = ModeloOltForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaModeloOlts')
        data['form'] = form
        return render(request, 'formModeloOlt.html', data)


def update_modeloOlt(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = ModeloOlt.objects.get(pk=pk)
        form = ModeloOltForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaModeloOlts')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formModeloOlt.html', data)


def delete_modeloOlt(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = ModeloOlt.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaModeloOlts')


class ModeloOnusView(TemplateView):
    template_name = 'listaModeloOnus.html'

    def get_context_data(self, **kwargs):
        context = super(ModeloOnusView, self).get_context_data(**kwargs)
        context['objetos'] = ModeloOnu.objects.all();
        return context


def novo_modeloOnu(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = ModeloOnuForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaModeloOnus')
        data['form'] = form
        return render(request, 'formModeloOnu.html', data)


def update_modeloOnu(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = ModeloOnu.objects.get(pk=pk)
        form = ModeloOnuForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaModeloOnus')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formModeloOnu.html', data)


def delete_modeloOnu(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = ModeloOnu.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaModeloOnus')


class OltsView(TemplateView):
    template_name = 'listaOlts.html'

    def get_context_data(self, **kwargs):
        context = super(OltsView, self).get_context_data(**kwargs)
        context['objetos'] = Olt.objects.all();
        return context


def novo_olt(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = OltForm(request.POST or None)
        if form.is_valid():
            ########################
            dados = form.save(commit=False)
            portas = int(dados.modelo.quantPortas)
            print(f'qtd de portas da cto = {portas}')
            form.save()
            ultimoObjeto = Olt.objects.last()
            print(f'Nome olt = {ultimoObjeto.nomeOlt}')
            #########
            print(f'id olt = {ultimoObjeto.id}')
            if ultimoObjeto.id==1:
                modo1 = Modo()
                modo1.nomeModo = 'bridge'
                modo1.save()
                modo2 = Modo()
                modo2.nomeModo = 'router'
                modo2.save()
            #########

            #cuidado! logo de primeira com o banco vazio não existe modo
            modo = Modo.objects.get(nomeModo='bridge')

            print(f'Nome modo = {modo.nomeModo}')
            for indice in range(1, (portas + 1)):
                print(f'Indice = {indice}')
                pon = Pon()
                pon.olt = ultimoObjeto
                pon.nomePon = ultimoObjeto.nomeOlt + '-gpon1/' + str(indice)
                pon.sinalPon = ''
                pon.portaPon = str(indice)
                print(pon.portaPon)
                pon.save()
                ultimoObjeto2 = Pon.objects.last()
                # modo.nomeModo='bridge'
                vlan = Vlan()
                vlan.modo = modo
                if indice < 10:
                    vlan.nomeValn = ultimoObjeto.nomeOlt + '-vlan10' + str(indice)
                    vlan.vlanID = '10' + str(indice)
                elif indice > 9:
                    vlan.nomeValn = ultimoObjeto.nomeOlt + '-vlan1' + str(indice)
                    vlan.vlanID = '1' + str(indice)
                vlan.pon = ultimoObjeto2
                vlan.save()

            modo1 = Modo.objects.get(nomeModo='router')
            vlan1 = Vlan()
            vlan1.modo = modo1
            vlan1.nomeValn = ultimoObjeto.nomeOlt + '-vlan120'
            vlan1.vlanID = '120'
            vlan1.save()
            ######################
            # form.save()
            return redirect('url_listaOlts')
        data['form'] = form
        return render(request, 'formOlt.html', data)


def update_olt(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = Olt.objects.get(pk=pk)
        form = OltForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaOlts')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formOlt.html', data)


def delete_olt(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = Olt.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaOlts')


def listaPonsDaOlt(request, pk):
    olt = Olt.objects.get(pk=pk)
    objetos_list = Pon.objects.filter(olt=olt).order_by('nomePon', 'portaPon');
    paginator = Paginator(objetos_list, 8)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    objetos = paginator.get_page(page_number)
    return render(request, 'listaPonsDaOlt.html', {'objetos': objetos})


class PonsView(TemplateView):
    template_name = 'listaPons.html'

    def get_context_data(self, **kwargs):
        context = super(PonsView, self).get_context_data(**kwargs)
        context['objetos'] = Pon.objects.all().order_by('portaPon');
        return context


def novo_pon(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = PonForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaPons')
        data['form'] = form
        return render(request, 'formPon.html', data)


def update_pon(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = Pon.objects.get(pk=pk)
        form = PonForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaOlts')
        data['form'] = form
        data['objetos'] = objeto
        return render(request, 'formPon.html', data)


def delete_pon(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = Pon.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaPons')


class ModosView(TemplateView):
    template_name = 'listaModos.html'

    def get_context_data(self, **kwargs):
        context = super(ModosView, self).get_context_data(**kwargs)
        context['objetos'] = Modo.objects.all();
        return context


def novo_modo(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = ModoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaModos')
        data['form'] = form
        return render(request, 'formModo.html', data)


def update_modo(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = Modo.objects.get(pk=pk)
        form = ModoForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaModos')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formCto.html', data)


def delete_modo(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = Modo.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaModos')


class VlansView(TemplateView):
    template_name = 'listaVlans.html'

    def get_context_data(self, **kwargs):
        context = super(VlansView, self).get_context_data(**kwargs)
        context['objetos'] = Vlan.objects.all().order_by('vlanID');
        return context


def listaVlans(request):
    #objetos_list = Vlan.objects.order_by('id').all().reverse()
    objetos_list = Vlan.objects.order_by('id').all()
    paginator = Paginator(objetos_list, 8)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    objetos = paginator.get_page(page_number)
    # ssh_connect('com')
    return render(request, 'listaVlans.html', {'objetos': objetos})


def novo_vlan(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = VlanForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaVlans')
        data['form'] = form
        return render(request, 'formVlan.html', data)


def update_vlan(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = Vlan.objects.get(pk=pk)
        form = VlanForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaVlans')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formVlan.html', data)


def delete_vlan(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = Vlan.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaVlans')


class CtosView(TemplateView):
    template_name = 'listaCtos.html'

    def get_context_data(self, **kwargs):
        context = super(CtosView, self).get_context_data(**kwargs)
        context['objetos'] = Cto.objects.all().order_by('id').reverse();
        return context


def listaCtos(request):
    objetos_list = Cto.objects.order_by('id').all().reverse()
    paginator = Paginator(objetos_list, 8)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    objetos = paginator.get_page(page_number)
    # ssh_connect('com')
    return render(request, 'listaCtos.html', {'objetos': objetos})


def novo_cto(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = CtoForm(request.POST or None)
        if form.is_valid():
            dados = form.save(commit=False)
            portas = int(dados.qtdPortas)
            print(f'qtd de portas da cto = {portas}')
            form.save()
            ultima_cto = Cto.objects.last()
            print(f'Nome cto = {ultima_cto.nomeCto}')

            for indice in range(1, (portas + 1)):
              portaCto = PortasCto()
              portaCto.cto = ultima_cto
              portaCto.numeroPorta = str(indice)
              portaCto.statusPorta = 'livre'
              print(portaCto.numeroPorta)
              print(portaCto.cto.nomeCto)
              print(portaCto.statusPorta)
              portaCto.save()
              #portaCto.close()
            return redirect('url_listaCtos')
        data['form'] = form
        return render(request, 'formCto.html', data)


def update_cto(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = Cto.objects.get(pk=pk)
        form = CtoForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaCtos')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formCto.html', data)


def delete_cto(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = Cto.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaCtos')


class OnusView(TemplateView):
    template_name = 'listaOnus.html'

    def get_context_data(self, **kwargs):
        context = super(OnusView, self).get_context_data(**kwargs)
        context['objetos'] = Onu.objects.all();
        return context


def novo_onu(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = OnuForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaOnus')
        data['form'] = form
        return render(request, 'formOnu.html', data)


def update_onu(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = Onu.objects.get(pk=pk)
        form = OnuForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaOnus')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formOnu.html', data)


def delete_onu(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = Onu.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaOnus')


class PortasCtosView(TemplateView):
    template_name = 'listaPortasCtos.html'

    def get_context_data(self, **kwargs):
        context = super(PortasCtosView, self).get_context_data(**kwargs)
        context['objetos'] = PortasCto.objects.all().order_by('id');
        return context


def PortasDaCto(request, pk):
    cto = Cto.objects.get(pk=pk)
    objetos_list = PortasCto.objects.filter(cto=cto, statusPorta='ocupada').order_by('id');
    paginator = Paginator(objetos_list, 4)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    objetos = paginator.get_page(page_number)
    return render(request, 'listaPortasDaCto.html', {'objetos': objetos})


def portaDeUmaCto(request, pk):
    objetos = PortasCto.objects.filter(pk=pk);
    return render(request, 'portaDeUmaCto.html', {'objetos': objetos})


def novo_portasCto(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        form = PortasCtoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('url_listaPortasCtos')
        data['form'] = form
        return render(request, 'formPortasCto.html', data)


def update_portasCto(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        data = {}
        objeto = PortasCto.objects.get(pk=pk)
        form = PortasCtoForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('url_listaPortasCtos')
        data['form'] = form
        data['cliente'] = objeto
        return render(request, 'formPortasCto.html', data)


def delete_portasCto(request, pk):
    if str(request.user) == 'AnonymousUser':
        return redirect('url_index')
    else:
        objeto = Onu.objects.get(pk=pk)
        objeto.delete()
        return redirect('url_listaPortasCtos')


# AJAX
def load_portasCto(request):
    cto_id = request.GET.get('cto_id')
    cto = Cto.objects.get(pk=cto_id)  # ok
    pon = cto.pon
    olt = pon.olt
    portasCto = PortasCto.objects.filter(cto_id=cto_id, statusPorta="livre").all()
    return render(request, 'dropdown.html', {'portasCto': portasCto, 'pon': pon, 'olt': olt})
    # return JsonResponse(list(portasCto.values('id', 'name')), safe=False)


def load_portasCto(request):
    cto_id = request.GET.get('cto_id')
    portasCto = PortasCto.objects.filter(cto_id=cto_id, statusPorta="livre").all()
    return render(request, 'dropdown.html', {'portasCto': portasCto})
    # return JsonResponse(list(portasCto.values('id', 'name')), safe=False)

