from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.utils import timezone

from perfis.views import get_perfil_logado
from .forms import PostagemForm
from .models import Postagem

class NovaPostagemView(View):

  def get(self, request):
    pass

  def post(self, request):
    form = PostagemForm(request.POST, request.FILES)
    if form.is_valid():
      dados = form.cleaned_data
      perfil = get_perfil_logado(request)
      imagem = form.verificar_imagem(request=request)
      postagem = Postagem.objects.create(
        perfil=perfil,
        conteudo=dados['conteudo'],
      )
      if imagem is not None:
        postagem.imagem = imagem
        postagem.save()
      return redirect('index')
    else:
      return render(request, 'index.html', {'form': form})

def ver_postagem(request, postagem_id):
  postagem = Postagem.objects.get(id=postagem_id)
  return render(request, 'postagem.html', {'perfil_logado': get_perfil_logado(request), 'postagem': postagem})

def apagar_postagem(request, postagem_id):
  postagem = Postagem.objects.get(id=postagem_id)
  postagem.delete()
  return redirect('index')

def editar_postagem(request, id):
  post = get_object_or_404(Postagem, id=id)
  new_content = request.GET.get('new_content', None)
  is_edited = post.edit(new_content)
  data = {'is_edited': is_edited}
  return JsonResponse(data)