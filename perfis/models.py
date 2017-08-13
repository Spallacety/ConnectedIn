from django.db import models
from django.contrib.auth.models import User
from timeline.models import Postagem

class Perfil(models.Model):

  QUESTOES = (
    (1, "Qual o ano de nascimento do seu pai?"),
    (2, "Qual o nome do seu animal de estimação?"),
    (3, "Onde você nasceu?"),
    (4, "Como é o nome da sua mãe?"),
  )

  nome = models.CharField(max_length=255, null=False)
  telefone = models.CharField(max_length=255, null=False)
  nome_empresa = models.CharField(max_length=255, null=False)
  amigos = models.ManyToManyField('self')
  bloqueados = models.ManyToManyField('self')
  usuario = models.OneToOneField(User, related_name='perfil')
  foto = models.ImageField(upload_to='avatars/', default='avatars/default.png', null=True)
  questao = models.CharField(max_length=1, null=False, choices=QUESTOES, default=1)
  resposta = models.CharField(max_length=128, null=False)
  desativado = models.BooleanField(default=False)

  @property
  def email(self):
    return self.usuario.email

  def convidar(self, perfil_convidado):
    c = Convite(solicitante = self, convidado = perfil_convidado)
    c.save()

  def bloquear(self, perfil_bloqueado):
    bloqueado = perfil_bloqueado
    b = Bloqueio(solicitante = self, bloqueado = perfil_bloqueado)
    self.bloqueados.add(bloqueado)
    b.save()

  def desbloquear(self, perfil_bloqueado):
    bloqueado = perfil_bloqueado
    b = Bloqueio.objects.filter(solicitante = self, bloqueado = perfil_bloqueado)
    self.bloqueados.remove(bloqueado)
    b.delete()

  def verificar_resposta(self, questao, resposta):
    return self.questao == questao and self.resposta == resposta

  def obter_postagens(self):
    return Postagem.objects.filter(perfil=self, visibilidade=True).distinct().order_by('-data_edicao')

  def obter_timeline(self):
    lista = self.obter_postagens()
    for amigo in self.amigos.all():
      if amigo not in self.bloqueados.all():
        lista = (lista | amigo.obter_postagens()).distinct()
    return lista[:20:1]

class Convite(models.Model):
  solicitante = models.ForeignKey(Perfil, related_name='convites_feitos')
  convidado = models.ForeignKey(Perfil, related_name='convites_recebidos')

  def aceitar(self):
    self.solicitante.amigos.add(self.convidado)
    self.convidado.amigos.add(self.solicitante)
    self.delete()

  def recusar(self):
    self.delete()

class Bloqueio(models.Model):
  solicitante = models.ForeignKey(Perfil, related_name='bloqueios_feitos')
  bloqueado = models.ForeignKey(Perfil, related_name='bloqueios_recebidos')