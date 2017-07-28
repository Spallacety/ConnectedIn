from datetime import timedelta
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone

class Postagem(models.Model):
  perfil = models.ForeignKey('perfis.Perfil', on_delete=CASCADE, related_name='postagens')
  conteudo = models.CharField(max_length=256, blank=True, null=False)
  imagem = models.ImageField(upload_to='postagens/', null=True)
  data_criacao = models.DateTimeField(null=False)
  data_edicao = models.DateTimeField(null=True)
  visibilidade = models.BooleanField(default=True, null=False)

  def editar(self, novo_conteudo):
    if self.editavel():
      self.conteudo = novo_conteudo
      self.data_edicao = timezone.now()
      self.save(force_update=True)
      return True
    else:
      return False

  def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    if self.data_criacao is None:
      self.data_criacao = timezone.now()
    if self.data_edicao is None:
      self.data_edicao = self.data_criacao
    super(Postagem, self).save(force_insert, force_update, using, update_fields)

  def delete(self, using=None, keep_parents=False):
    self.visibilidade = False
    self.save()

  def editavel(self):
    return (self.data_criacao + timedelta(seconds=59)) > timezone.now() and not self.imagem