from django.urls import path
from .views import *

urlpatterns = [
    path('home', IndexView.as_view(), name='url_index'),
   # path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX
    path('ajax/load-portasCto/', load_portasCto, name='ajax_load_portasCto'),  # AJAX
    #path('', ProvisionadosView.as_view(), name='url_listaProvisionados'),
    path('', listaProvisionados, name='url_listaProvisionados'),
    path('listaProvisionadosOrder/<str:pk>', listaProvisionadosOrder, name='url_listaProvisionadosOrder'),
    path('listaFabricantes', FabricantesView.as_view(), name='url_listaFabricantes'),
    path('listaModeloOlts', ModeloOltsView.as_view(), name='url_listaModeloOlts'),
    path('listaModeloOnus', ModeloOnusView.as_view(), name='url_listaModeloOnus'),

    #path('listaVlans', VlansView.as_view(), name='url_listaVlans'),
    path('listaVlans', listaVlans, name='url_listaVlans'),

    path('listaClientes', ClientesView.as_view(), name='url_listaClientes'),
    #path('listaCtos', CtosView.as_view(), name='url_listaCtos'),
    path('listaCtos', listaCtos, name='url_listaCtos'),
    path('listaModos', ModosView.as_view(), name='url_listaModos'),
    path('listaOlts', OltsView.as_view(), name='url_listaOlts'),
    path('listaOnus', OnusView.as_view(), name='url_listaOnus'),
    path('listaPlanos', PlanosView.as_view(), name='url_listaPlanos'),
    path('listaPons', PonsView.as_view(), name='url_listaPons'),
    path('listaPonsDaOlt/<int:pk>', listaPonsDaOlt, name='url_listaPonsDaOlt'),
    path('listaPortasCtos', PortasCtosView.as_view(), name='url_listaPortasCtos'),
    path('listaPortasDaCto/<int:pk>', PortasDaCto, name='url_listaPortasDaCto'),
path('portaDeUmaCto/<int:pk>', portaDeUmaCto, name='url_portaDeUmaCto'),

    path('formFabricante', novo_fabricante, name='url_novo_fabricante'),

    path('provisionar/', novo_provisionamento, name='url_nova_provisionamento'),
    path('update_provisionamento/<int:pk>', update_provisionamento, name='url_update_provisionamento'),
    path('delete_provisionamento/<int:pk>', delete_provisionamento, name='url_delete_provisionamento'),

    path('novo_cliente/', novo_cliente, name='url_novo_cliente'),
    path('update_cliente/<int:pk>', update_cliente, name='url_update_cliente'),
    path('delete_cliente/<int:pk>', delete_cliente, name='url_delete_cliente'),

    path('novo_plano/', novo_plano, name='url_novo_plano'),
    path('update_plano/<int:pk>', update_plano, name='url_update_plano'),
    path('delete_plano/<int:pk>', delete_plano, name='url_delete_plano'),

    path('novo_fabricante/', novo_fabricante, name='url_novo_fabricante'),
    path('update_fabricante/<int:pk>', update_fabricante, name='url_update_fabricante'),
    path('delete_fabricante/<int:pk>', delete_fabricante, name='url_delete_fabricante'),

    path('novo_modeloOlt/', novo_modeloOlt, name='url_novo_modeloOlt'),
    path('update_modeloOlt/<int:pk>', update_modeloOlt, name='url_update_modeloOlt'),
    path('delete_modeloOlt/<int:pk>', delete_modeloOlt, name='url_delete_modeloOlt'),

    path('novo_modeloOnu/', novo_modeloOnu, name='url_novo_modeloOnu'),
    path('update_modeloOnu/<int:pk>', update_modeloOnu, name='url_update_modeloOnu'),
    path('delete_modeloOnu/<int:pk>', delete_modeloOnu, name='url_delete_modeloOnu'),

    path('novo_olt/', novo_olt, name='url_novo_olt'),
    path('update_olt/<int:pk>', update_olt, name='url_update_olt'),
    path('delete_olt/<int:pk>', delete_olt, name='url_delete_olt'),

    path('novo_pon/', novo_pon, name='url_novo_pon'),
    path('update_pon/<int:pk>', update_pon, name='url_update_pon'),
    path('delete_pon/<int:pk>', delete_pon, name='url_delete_pon'),

    path('novo_modo/', novo_modo, name='url_novo_modo'),
    path('update_modo/<int:pk>', update_modo, name='url_update_modo'),
    path('delete_modo/<int:pk>', delete_modo, name='url_delete_modo'),

    path('novo_vlan/', novo_vlan, name='url_novo_vlan'),
    path('update_vlan/<int:pk>', update_vlan, name='url_update_vlan'),
    path('delete_vlan/<int:pk>', delete_vlan, name='url_delete_vlan'),

    path('novo_cto/', novo_cto, name='url_novo_cto'),
    path('update_cto/<int:pk>', update_cto, name='url_update_cto'),
    path('delete_cto/<int:pk>', delete_cto, name='url_delete_cto'),

    path('novo_onu/', novo_onu, name='url_novo_onu'),
    path('update_onu/<int:pk>', update_onu, name='url_update_onu'),
    path('delete_onu/<int:pk>', delete_onu, name='url_delete_onu'),

    path('novo_portasCto/', novo_portasCto, name='url_novo_portasCto'),
    path('update_portasCto/<int:pk>', update_portasCto, name='url_update_portasCto'),
    path('delete_portasCto/<int:pk>', delete_portasCto, name='url_delete_portasCto')
]
