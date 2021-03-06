from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.db.models import Q
from .forms import *
from perfis.models import *
from perfis.views import get_perfil_logado

class RegistrarUsuarioView(View):
  template = 'registrar.html'

  def get(self, request):
    return render(request, self.template)

  def post(self, request):
    form = RegistrarUsuarioForm(request.POST)

    if form.is_valid():
      dados_form = form.cleaned_data
      usuario = User.objects.create_user(username=dados_form['email'], email=dados_form['email'], password=dados_form['senha'])
      perfil = Perfil(nome=dados_form['nome'], telefone=dados_form['telefone'], nome_empresa=dados_form['nome_empresa'], usuario=usuario, questao=dados_form['questao'], resposta=dados_form['resposta'])
      perfil.save()
      return redirect('index')

    return render(request, self.template, {'form': form})

class EditarUsuarioView(View):
  template = 'editar.html'

  def get(self, request):
    form = EditarUsuarioForm()
    perfil = get_perfil_logado(request)

    return render(request, self.template, {'form': form, 'perfil': perfil})

  def post(self, request):
    form = EditarUsuarioForm(request.POST, request.FILES)

    if form.is_valid():
      dados_form = form.cleaned_data
      perfil = get_perfil_logado(request)
      perfil.nome = dados_form['nome']
      perfil.telefone = dados_form['telefone']
      perfil.nome_empresa = dados_form['nome_empresa']
      perfil.questao = dados_form['questao']
      perfil.resposta = dados_form['resposta']
      foto = form.verificar_foto(request)
      if foto is not None:
        perfil.foto = foto
      perfil.save()

      return redirect('perfil', perfil.id)

    return render(request, self.template, {'form': form})

class AlterarSenhaView(View):
  def get(self, request):
    return render(request, 'alterar_senha.html')

  def post(self, request):
    perfil = get_perfil_logado(request)
    user = User.objects.get(id=perfil.usuario.id)

    form = AlterarSenhaForm(request.POST, request=request)

    if form.is_valid():
      dados_form = form.cleaned_data
      user.set_password(dados_form['nova_senha1'])
      user.save()
      return redirect('index')

    return render(request, 'alterar_senha.html', {'form': form})

class RecuperarSenhaView(View):
  def get(self, request):
    return render(request, 'recuperar_senha.html')

  def post(self, request):
    form = RecuperarSenhaForm(request.POST)

    if form.is_valid():
      dados_form = form.cleaned_data
      try:
        user = User.objects.get(username=dados_form['email'])
        perfil = Perfil.objects.get(usuario=user, questao=dados_form['questao'], resposta=dados_form['resposta'])
        if perfil:
          user.set_password('123')
          user.save()
        return redirect('index')
      except:
        return redirect('index')

    return render(request, 'recuperar_senha.html', {'form': form})

class BuscarView(View):
  def get(self, request):
    return render(request, 'buscar.html')

  def post(self, request):
    form = BuscarForm(request.POST)

    if form.is_valid():
      dados_form = form.cleaned_data
      condicao = Q(nome__icontains=dados_form['nome'])
      perfis = Perfil.objects.filter(condicao)
      return render(request, 'buscar.html', {'perfis': perfis})

    return render(request, 'buscar.html', {'form': form})