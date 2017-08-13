from django import forms
from django.contrib.auth.models import User
from perfis.views import get_perfil_logado
from perfis.models import Perfil

class RegistrarUsuarioForm(forms.Form):
  email = forms.EmailField(required=True)
  senha = forms.CharField(required=True)
  nome = forms.CharField(required=True)
  telefone = forms.CharField(required=True)
  nome_empresa = forms.CharField(required=True)
  questao = forms.ChoiceField(choices=Perfil.QUESTOES, required=True)
  resposta = forms.CharField(required=True)

  def is_valid(self):
    valid = True

    if not super(RegistrarUsuarioForm, self).is_valid():
      self.adiciona_erro('Por favor, verifique os dados informados.')
      valid = False

    user_exists = User.objects.filter(username=self.data['email']).exists()
    if user_exists:
      self.adiciona_erro('E-mail já cadastrado.')
      valid = False

    return valid

  def adiciona_erro(self, message):
    errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())

    errors.append(message)

class EditarUsuarioForm(forms.Form):

  nome = forms.CharField(required=True)
  foto = forms.ImageField(required=False)
  telefone = forms.CharField(required=True)
  nome_empresa = forms.CharField(required=True)

  def verificar_foto(self, request):
    if 'foto' in request.FILES and (request.FILES['foto'] is not None or request.FILES['foto'] is not ''):

      foto = self.cleaned_data['foto']

      try:
        main, sub = foto.content_type.split('/')
        if not (main == 'image' and sub in ['jpeg', 'jpg', 'png']):
          raise forms.ValidationError(u'Please use a JPEG, JPG or PNG image.')

      except AttributeError:
        """
        Handles case when we are updating the user profile
        and do not supply a new avatar
        """
        pass

      return foto
    else:
      return None

  def is_valid_from_form(self):
    return super(EditarUsuarioForm, self).is_valid()

class AlterarSenhaForm(forms.Form):
  velha_senha = forms.CharField(required=True)
  nova_senha1 = forms.CharField(required=True)
  nova_senha2 = forms.CharField(required=True)

  def is_valid(self):
    valid = True

    if not super(AlterarSenhaForm, self).is_valid():
      self.adiciona_erro('Por favor, verifique os dados informados.')
      valid = False

    valid_pass = get_perfil_logado(self.request).usuario.check_password(self.data['velha_senha'])
    if not valid_pass:
      self.adiciona_erro('A senha digitada está incorreta.')
      valid = False

    pass_not_match = (self.data['nova_senha1'] != self.data['nova_senha2'])
    if pass_not_match:
      self.adiciona_erro('As novas senhas são diferentes.')
      valid = False

    return valid

  def adiciona_erro(self, message):
    errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())

    errors.append(message)

  def __init__(self, *args, **kwargs):
    self.request = kwargs.pop('request', None)
    super(AlterarSenhaForm, self).__init__(*args, **kwargs)

class RecuperarSenhaForm(forms.Form):
  email = forms.EmailField(required=True)
  questao = forms.ChoiceField(choices=Perfil.QUESTOES, required=True)
  resposta = forms.CharField(required=True)

  def is_valid(self):
    valid = True

    if not super(RecuperarSenhaForm, self).is_valid():
      self.adiciona_erro('Por favor, verifique os dados informados.')
      valid = False

    return valid

  def adiciona_erro(self, message):
    errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())

    errors.append(message)

class BuscarForm(forms.Form):
  nome = forms.CharField(required=True)