"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
import api.views as views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.page_r1, name='home'),
    path('cadastroPiloto/', views.pilot_registration, name='cadastro_piloto'),
    re_path(r'^cadastroPiloto/edit/(?P<pk>[\w.-]+)/$', views.pilot_registration, name='cadastro_piloto_edit'),
    path('pilotosCadastrados/', views.pilot_list, name='pilot_list'),
    path('cadastroFazenda/', views.farm_registration, name='cadastro_fazenda'),
    path('cadastroFazenda/edit/<str:idf>/', views.farm_registration, name='cadastro_fazenda_edit_f'),
    path('cadastroFazenda/edit-talhao/<int:idt>/', views.farm_registration, name='cadastro_fazenda_edit_t'),
    path('fazendasCadastradas/', views.farm_list, name='farm_list'),
    path('fazendasCadastradas2/', views.farm_list2, name='farm_list2'),
    path('FazendaseTalhoes/', views.farm_talhao_list, name='farm_talhao_list'),
    path('FazendaseTalhoes2/', views.farm_talhao_list2, name='farm_talhao_list2'),
    path('cadastroProduto/', views.product_registration, name='cadastro_produto'),
    path('cadastroProduto/edit/<int:pk>', views.product_registration, name='cadastro_produto_edit'),
    path('relatorioProdutos/', views.product_list, name='product_list'),
    path('relatorioProdutos2/', views.product_list2, name='product_list2'),
    path('cadastroAeronave/', views.aeronave_registration, name='cadastro_aeronave'),
    path('cadastroAeronave/edit/<str:pk>/', views.aeronave_registration, name='cadastro_aeronave_edit'),
    path('aeronavesCadastradas/', views.aeronave_list, name='aeronave_list'),
    path('aeronavesCadastradas2/', views.aeronave_list2, name='aeronave_list2'),
    re_path(r'^fetch-data/(?P<pk>[\w.-]+)/$', views.fetch_data_view, name='fetch_data'),  # For fetching data
    path('fetch-data-farm/<int:pk>/', views.fetch_data_farm_view, name='fetch_data_farm'),  # For fetching data
    path('cadastro_guia/', views.guia_aplicacao, name='cadastro_guia'),
    path('cadastro_guia/edit/<int:id>', views.guia_aplicacao, name='cadastro_guia_edit'),
    path('fetch-data-guia-farm/<str:pk>/', views.fetch_data_guia_farm, name='fetch_data_guia_farm'),  # For fetching data
    path('fetch-data-guia-prod/<str:pk>/', views.fetch_data_guia_prod, name='fetch_data_guia_prod'),  # For fetching data
    path('fetch-data-guia-talhao/', views.fetch_data_guia_talhao, name='fetch_data_guia_talhao'),  # For fetching data
    path('guiasCadastradas/', views.guia_aplicacao_list, name='guia_aplicacao_list'),
    path('guiaAplicacaoPiloto/', views.guia_aplicacao_piloto, name='guia_aplicacao_piloto'),
    path('homePiloto/', views.page_r2, name='homePiloto'),
    path('guiaPiloto/', views.guia_aplicacao_piloto, name='guia_piloto'),
    re_path(r'^guiaPiloto/edit/(?P<pk>[\w.-]+)/$', views.guia_aplicacao_piloto, name='guia_piloto_edit'),
    path('guiasCadastradasPiloto/', views.guia_piloto_list, name='guia_piloto_list'),
    path('fetch-guia-piloto/<int:parent_id>/', views.fetch_guia_piloto, name='fetch_guia_piloto'),
    re_path(r'^edit-piloto/(?P<pk>[\w.-]+)/$', views.edit_pilot, name='edit_pilot'),
    path('edit-aeronave/<str:pk>/', views.edit_aeronave, name='edit_aeronave'),
    path('edit-produto/<int:pk>/', views.edit_product, name='edit_product'),
    path('edit-farm/<str:pk>/', views.edit_farm, name='edit_farm'),
    path('edit-talhao/<str:pk>/', views.edit_talhao, name='edit_talhao'),
    path('edit-guia/<int:pk>/', views.edit_guia, name='edit_guia'),
    path('edit-guia-piloto/<int:pk>/', views.edit_guia_piloto, name='edit_guia_piloto'),
    path('get-images/<int:id>/', views.get_images_piloto, name='get_images'),
]
