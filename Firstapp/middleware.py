# Django
# Para nuestro objetivo ocuparemos redirect para que el usuario
# se dirija a la configuración en caso de no cumplir con los requisitos.
from django.shortcuts import redirect
# Usaremos reverse para hacer referencia al alias
# de los path de nuestro proyecto.
from django.urls import reverse

class ProfileCompletionMiddleware:
  # Este __init__ siempre ira, asi que es fundamental al crear tu clase
  def __init__(self, get_response):
    self.get_response = get_response

  # Dentro de __call__ es donde realizaremos nuestras validaciones.
  def __call__(self, request):
    # En caso de que el usuario no sea anonimo.
    if not request.user.is_anonymous:
      profile = request.user.profile
      
      # Verificamos que la instacia de user tenga
      # una foto o biografía.
      if not profile.picture or not profile.biography:
        # En caso de que no trate de navegar al path de
        # 'update_profile' o 'logout'
        if request.path not in [reverse('update_profile'), reverse('logout')]:
          # Vamos a redireccionarlo al path de 'update_profile'
          return redirect('update_profile')

    # En caso de que cumple todos los requisitos devolvemos la solicitud original.
    response = self.get_response(request)
    return response