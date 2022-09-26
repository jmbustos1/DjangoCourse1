from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# Forms
from goodapp.forms import PostForm
# Models
from goodapp.models import Post


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


# Create your views here.
pics= [
    {
        'title': 'Mont Blanc',
        'user': {
            'name': 'Yésica Cortés',
            'picture': 'https://picsum.photos/60/60/?image=1027'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/800/600?image=1036',
    },
    {
        'title': 'Via Láctea',
        'user': {
            'name': 'Christian Van der Henst',
            'picture': 'https://picsum.photos/60/60/?image=1005'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/800/800/?image=903',
    },
    {
        'title': 'Nuevo auditorio',
        'user': {
            'name': 'Uriel (thespianartist)',
            'picture': 'https://picsum.photos/60/60/?image=883'
        },
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'photo': 'https://picsum.photos/500/700/?image=1076',
    }
]
def list_posts(request):
    return render(request, 'feed.html', {'pics': pics})

def list_posts2(request):
  posts = [1, 2, 3, 4]
  return HttpResponse(str(posts))


def list_posts3(request):
    # En la función que nos devuelve el render, debemos referenciar correctamente el template, 
    # en este caso a posts/feed.html
    return render(request, 'goodapp/feed.html', {'pics': pics})

# Decoramos con login_required la función que renderiza nuestra vista, 
# el cual ahora necesitara una sesión iniciada para poder renderizarse. 
# En caso de no estarlo nos redirigira al path de login.
@login_required
def list_posts4(request):
  """
  View to lists posts
  """
  posts = Post.objects.all().order_by('-created')
  return render(request, 'goodapp/feed.html', {'pics': pics})



@login_required
def create_post(request):
    """Create new post view."""

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.profile = request.user.profile
            form.save()
            return redirect('goodapp:feed')

    else:
        form = PostForm()

    return render(
        request=request,
        template_name='goodapp/new.html',
        context={
            'form': form,
            'user': request.user,
            'profile': request.user.profile
        }
    )


class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts."""

    # Enviamos em template
    template_name = 'goodapp/feed.html'
    # El modelo que listaremos
    model = Post
    # El orden
    ordering = ('-created',)
    # Paginamos
    paginate_by = 2
    # Enviamos el objeto al html como posts
    context_object_name = 'goodapp'