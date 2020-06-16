from django.urls import include, re_path
from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from AppGF.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', registro, name='registro'),
    
    path('usuario/', UsuarioList.as_view(), name="usuarios_list"),

    re_path('usuario/update/(?P<pk>\d+)', UsuarioUpdate.as_view(), name="usuarios_update"),
    path('usuario/detail/<int:pk>', UsuarioDetail.as_view(), name="usuarios_detail"),
    path('usuario/delete/<int:pk>', UsuarioDelete.as_view(), name="usuarios_delete"),
    path('pescado/', PescadoList.as_view(), name="pescados_list"),
    path('pescado/create/', PescadoCreate.as_view(), name="pescados_create"),
    path('pescado/detail/<int:pk>', PescadoDetail.as_view(), name="pescados_detail"),
    path('zonapesca/', ZonaPescaList.as_view(), name="zonapesca"),
    path('zonapesca/create/', ZonaPescaCreate.as_view(), name="zonapescas_create"),
    path('señuelo/', SeñueloList.as_view(), name="señuelo"),
    path('captura/', CapturaList.as_view(), name="capturas_list"),
    path('captura/detail/<int:pk>', CapturaDetail.as_view(), name="captura_detail"),
    re_path('captura/update/(?P<pk>\d+)', CapturaUpdate.as_view(), name="capturas_update"),
    re_path('captura/delete/(?P<pk>\d+)', CapturaDelete.as_view(), name="capturas_delete"),
    re_path(r'^captura/detail/(?P<username>\w+)/$', CapturaListUsu.as_view(), name="capturas_usu_list"),
    path('captura/create/', crearCaptura, name="capturas_create"),
    
    path('sugerencias/', contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
