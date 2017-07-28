from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^postagem/$', NovaPostagemView.as_view(), name="nova_postagem"),
    url(r'^postagem/(?P<postagem_id>\d+)/$', ver_postagem, name="ver_postagem"),
    url(r'^postagem/(?P<postagem_id>\d+)/editar$', editar_postagem, name="editar_postagem"),
    url(r'^postagem/(?P<postagem_id>\d+)/apagar$', apagar_postagem, name="apagar_postagem"),
]