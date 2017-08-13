from django.conf.urls import url
from .views import *
from django.contrib.auth import views

urlpatterns = [
  url(r'^registrar/$', RegistrarUsuarioView.as_view(), name='registrar'),
  url(r'^editar/$', EditarUsuarioView.as_view(), name='editar'),
  url(r'^login/$', views.LoginView.as_view(template_name='login.html'), name='login'),
  url(r'^logout/$', views.LogoutView.as_view(template_name='login.html'), name='logout'),
  url(r'^alterar_senha$', AlterarSenhaView.as_view(), name='alterar_senha'),
  url(r'^recuperar_senha$', RecuperarSenhaView.as_view(), name='recuperar_senha'),
  url(r'^buscar$', BuscarView.as_view(), name='buscar'),
]