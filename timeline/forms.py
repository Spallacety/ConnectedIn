from django import forms

class PostagemForm(forms.Form):
  conteudo = forms.CharField(max_length=256, required=True)
  imagem = forms.ImageField(required=False)

  def verificar_imagem(self, request):
    if 'imagem' in request.FILES and (request.FILES['imagem'] is not None or request.FILES['imagem'] is not ''):
      imagem = request.FILES['imagem']
      try:
        main, sub = imagem.content_type.split('/')
        if not (main == 'image' and sub in ['jpeg', 'jpg', 'png']):
          raise forms.ValidationError(u'Apenas imagens nos formatos JPEG, JPG ou PNG são aceitos.')
      except AttributeError:
        pass
      return imagem
    else:
      return None