from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^perfil/(?P<perfil_id>\d+)$', views.perfil, name='perfil'),
    url(r'^perfil/(?P<perfil_id>\d+)/convidar$', views.convidar, name='convidar'),
    url(r'^perfil/(?P<perfil_id>\d+)/remover$', views.remover_amizade, name='remover_amizade'),
    url(r'^convite/(?P<convite_id>\d+)/aceitar$', views.aceitar, name='aceitar'),
    url(r'^convite/(?P<convite_id>\d+)/recusar$', views.recusar, name='recusar'),
    url(r'^perfil/(?P<perfil_id>\d+)/bloquear$', views.bloquear, name='bloquear'),
    url(r'^perfil/(?P<perfil_id>\d+)/desbloquear$', views.desbloquear, name='desbloquear'),
]