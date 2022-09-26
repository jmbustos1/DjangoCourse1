"""Firstapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from Firstapp import views
from django.conf.urls.static import static

from goodapp import views as goodapp_views

from users import views as users_views

from django.conf import settings
#def hello_world(request):
#    return HttpResponse("Hello, world!")

urlpatterns = [
    path('admin/', admin.site.urls), #admin
    path('hello-world/', views.hello_world), #simple View
    path('numbers/', views.numbers), # Uso de GET and POST request.method
    path('hi/<str:name>/<int:age>/', views.say_hi), # Pasando argumentos por URL

    path('goodapp/', goodapp_views.list_posts2),
    path('goodapp2/', goodapp_views.list_posts),
    path('goodapp3/', goodapp_views.list_posts3),
    
    path("", include(("goodapp.urls", "posts"), namespace="goodapp")),
    path("users/", include(("users.urls", "users"), namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
