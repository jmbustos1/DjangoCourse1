"""
User admin classes.
"""

from django.contrib import admin
# Importamos UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import User
from users.models import Profile
from PIL import Image
# Registramos nuestros modelos aquí.
# admin.site.register(Profile)
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): #Por convencion la clase que creemos debe terminar en Admin.

  # Con list_display nombramos los campos que queremos visualizar.
  list_display = ('pk', 'user', 'phone_number', 'website', 'picture')

  # list_display_links establece como links los campos nombrados.
  list_display_links = ('pk', 'user')

  # list_editable nos permite editar el campo desde 
  # la lista del modelo en vez de ingresar al detalle del registro.
  list_editable = ('phone_number','picture')

  # Para crear un buscador hacemos uso de search_fields. 
  # Los campos que se ingresan seran los que el buscador recorrera para realizar las busquedas.
  search_fields = (
    'user__email',
    'user__username', 
    'user__first_name', 
    'user__last_name', 
    'phone_number'
  )

  # Podemos crear un filtro para nuestro dashboard del modelo, 
  # para ello usamos list_filter, y definimos los campos con los que trabajara.
  list_filter = (
    'user__is_active',
    'user__is_staff',
    'created', 
    'modified'
  )

  # Nos desplagara los datos que deseamos. Es importante que la información
  # este en tuplas.
  fieldsets = (
        (
            "Profile", { # Nombre de la sección o titulo
                "fields": ( # Los campos que visualizaremos.

                        # Cuando declaramos varios campos en la misma tupla
                        # se va a desplegar los datos en la misma fila.
                        ("user", "picture"),
                    ),
                }
        ),
        (
            "Extra info", {
                "fields": (

                        # En este caso la información se desplegara en 2 filas
                        # ya que la tupla de fields tiene 2 tuplas.
                        ("website", "phone_number"),
                        ("biography"),
                    ),
            }
        ),
        (
            "Meta data", {
                "fields": (
                    # Estos datos no se pueden modificar, ya que, en el modelo
                    # se declaro que no son editables, por lo que haremos uso
                    # de readonly_fields.
                    ("created", "modified"),
                )
            }

        ),
    )
  # Aqui declararemos los campos que solo pueden ser leidos pero no
  # modificados.
  readonly_fields = ("created", "modified")

# Para incluir el módelo Profile en el módelo User, hacemos lo siguiente.
class ProfileInline(admin.StackedInline):
    """
    En esta clase definiremos el modelo que deseamos asociar a User, en nuestro
    caso Profile.
    """

    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"

# Luego para asociar los modelos e insertarlo en el Dashboard usaremos
# el UserAdmin de Django el cual le dimos el alias de BaseUserAdmin.
class UserAdmin(BaseUserAdmin):
    """
    Add Profile admin to base user admin.
    """

    inlines = (ProfileInline,)
    list_display = ( # En list_display
    "username",
    "email",
    "first_name",
    "last_name",
    "is_active",
    "is_staff",
  )

# Re-register UserAdmin
admin.site.unregister(User)
# Le pasamos el modelo y la clase que va a usar
admin.site.register(User, UserAdmin)