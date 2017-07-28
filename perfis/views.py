from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from timeline.models import *

@login_required
def index(request):
  return render(request, 'index.html', {'perfil_logado': get_perfil_logado(request)})

@login_required
def perfil(request, perfil_id):

  perfil = Perfil.objects.get(id=perfil_id)
  is_friend = perfil in get_perfil_logado(request).amigos.all()
  requesting = False
  requested = False
  blocked = False
  blocking = False

  try:
    if get_perfil_logado(request) == perfil.convites_recebidos.get(solicitante=get_perfil_logado(request)).solicitante:
      requesting = True
      convite = perfil.convites_recebidos.get(solicitante=get_perfil_logado(request))
  except:
    requesting = False
    convite = Convite()

  try:
    if perfil == get_perfil_logado(request).convites_recebidos.get(solicitante=perfil).solicitante:
      requested = True
      convite = get_perfil_logado(request).convites_recebidos.get(solicitante=perfil)
  except:
    requested = False
    convite = Convite()

  try:
    if get_perfil_logado(request) == perfil.bloqueios_feitos.get(solicitante=perfil, bloqueado=get_perfil_logado(request)).bloqueado:
      blocked = True
  except:
    blocked = False

  try:
    if perfil == get_perfil_logado(request).bloqueios_feitos.get(solicitante=get_perfil_logado(request), bloqueado=perfil).bloqueado:
      blocking = True
  except:
    blocking = False

  return render(request, 'perfil.html', {'perfil': perfil, 'perfil_logado': get_perfil_logado(request), 'is_friend': is_friend, 'requesting': requesting, 'requested': requested, 'convite': convite, 'blocked': blocked, 'blocking': blocking})

@login_required
def convidar(request, perfil_id):
  perfil_convidado = Perfil.objects.get(id=perfil_id)
  perfil_logado = get_perfil_logado(request)
  perfil_logado.convidar(perfil_convidado)
  return redirect('perfil', perfil_id)

@login_required
def remover_amizade(request, perfil_id):
  perfil = Perfil.objects.get(id=perfil_id)
  perfil_logado = get_perfil_logado(request)
  perfil.amigos.remove(get_perfil_logado(request))
  perfil_logado.amigos.remove(perfil)
  return redirect('perfil', perfil_id)

@login_required
def aceitar(request, convite_id):
  convite = Convite.objects.get(id = convite_id)
  convite.aceitar()
  return redirect('index')

@login_required
def recusar(request, convite_id):
  convite = Convite.objects.get(id = convite_id)
  convite.recusar()
  return redirect('index')

@login_required
def bloquear(request, perfil_id):
  perfil_bloqueado = Perfil.objects.get(id=perfil_id)
  perfil_logado = get_perfil_logado(request)
  perfil_logado.bloquear(perfil_bloqueado)
  return redirect('perfil', perfil_id)

@login_required
def desbloquear(request, perfil_id):
  perfil_bloqueado = Perfil.objects.get(id=perfil_id)
  perfil_logado = get_perfil_logado(request)
  perfil_logado.desbloquear(perfil_bloqueado)
  return redirect('perfil', perfil_id)

@login_required
def get_perfil_logado(request):
  return request.user.perfil