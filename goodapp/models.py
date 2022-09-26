from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from users.models import Profile
class Post(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # Con ForeignKey podemos relacionar el modelo de posts con profile, 
  # y para hacer referencia a la clase relacionada lo hacemos con 
  # el formato de 'aplicacion.NombreClaseDelModelo'.
  profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

  title = models.CharField(max_length=255)
  photo = models.ImageField(upload_to='post/photos')

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return '{} by @{}'.format(self.title, self.user.username)
    
# class User(models.Model):
#     """
#     User Model
#     """
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     bio = models.TextField(blank=True)
#     birthdate = models.DateField(blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#     is_admin = models.BooleanField(default=False)