from django.shortcuts import render
from django.contrib.auth import views as auth_views
# Create your views here.
# Django
# Importamos authenticate y login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Importamos posible error al tratar de crear una instancia con valor único que ya existe
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
# Importamos los modelos de las instancias que crearemos
from django.contrib.auth.models import User
from users.models import Profile
# Importamos el ProfileForm que creamos anteriormente
from users.forms import ProfileForm
from users.forms import SignupForm
# Redirect nos ayudara a redireccionarnos a otro path
from django.shortcuts import redirect, render
from django.views.generic import DetailView, FormView, UpdateView
from goodapp.models import Post
from users.forms import ProfileForm, SignupForm
from django.urls import reverse, reverse_lazy

class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view."""

    template_name = "users/detail.html"

    # Es el campo que se la pasara a la query para buscar el usuario
    # Podemos pasarle <email> tambien, esta vez buscamos el usuario por su
    # username
    slug_field = "username"

    # Es la palabra clave que le pasamos al url detail/<str:username>/
    slug_url_kwarg = "username"

    queryset = User.objects.all()

    # Esto es como se mandara el objeto al html
    context_object_name = "user"

    # Sobre escribimos el método get_context_data
    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["goodapp"] = Post.objects.filter(user=user).order_by("-created")
        return context


def signup(request):
  if request.method == 'POST':
    # Le enviamos los datos de request a nuestro formulario
    form = SignupForm(request.POST)
    
    # En caso de ser valido guarda las instancias
    # y nos redirige al login.
    if form.is_valid():
      form.save()
      return redirect('login')
  
  else:
    form = SignupForm()

  return render(
    request=request,
    template_name='users/signup.html',
    context={
      'form': form
    }
  )

def login_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    # El metodo authenticate tratara de contrastar el usuario 
    # con una instancia del modelo users que creamos.
    user = authenticate(request, username=username, password=password)
    if user:
      # En caso de ser exitoso la autenticación creara 
      # un token de nuestro usuario para almacenarlo en memoria.
      login(request, user)
      # Y nos redireccionaremos al path con alias 'feed' que es 'posts/'
      return redirect('goodapp:feed')
    else:
      # En caso de dar false la autenticacion volveremos a renderizar el login, 
      # pero enviando la variable 'error'
      return render(request, 'users/login.html', {'error': 'Invalid username and password'})
  return render(request, 'users/login.html')


@login_required
def logout_view(request):
  logout(request) # Ejecutamos logout, el cual borrara los tokens del navegador.
  return redirect('users:login') # Redirigimos a path de login.

# En la vista de update_profile vamos a recibir el request.
# users/views.py
@login_required
def update_profile2(request):
    """
    Update a user's profile view
    """
    # Crearemos una variable que guardara el profile
    # que esta realizando el request.
    profile = request.user.profile

    # Si el request es de tipo 'POST'
    if request.method == "POST":

        # Crearemos una instancia de ProfileForm
        # con los datos que recibimos a traves de request
        form = ProfileForm(request.POST, request.FILES)

        # Si la instacia se crea sin problemas.
        if form.is_valid():

            # Guardaremos los datos recibidos en base de datos.
            data = form.cleaned_data

            profile.website = data["website"]
            profile.phone_number = data["phone_number"]
            profile.biography = data["biography"]
            if data["picture"]:
                profile.picture = data["picture"]
            profile.save()

            # Y redireccionaremos a la pagina update_profile para reflejar los
            # cambios. Como detail, espera un argumento debemos usar reverse
            # y pasarle el argumento en los kwargs
            url = reverse(
                'users:detail',
                kwargs={'username': request.user.username},
            )
            return redirect(url)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = "users/update_profile.html"
    model = Profile
    fields = ["website", "biography", "phone_number", "picture"]

    def get_object(self):
        """Return user's profile."""
        # Retorna el objeto profile
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""

        # self.obejct es el profile que retornamos en get_object
        username = self.object.user.username

        return reverse("users:detail", kwargs={"username": username})


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = "users/login.html"

