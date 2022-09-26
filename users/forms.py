# Django
from django import forms

# Models
from django.contrib.auth.models import User
from users.models import Profile

class SignupForm(forms.Form):
    """
    Signup Form
    """

    # Definimos los campos.
    username = forms.CharField(min_length=4, max_length=50)

    password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(),
    )

    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(),
    )

    # verificamos que el username no exista. El nombre de la clase debe ser
    # clean_<field>, en este caso el field es username
    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            #  En caso de existir devolvemos un mensaje de error al html.
            raise forms.ValidationError('Username is already in use.')
        # Siempre debemos retornar el campo
        return username

    # Sobreescribimos el método clean
    def clean(self):
        # Llamamos el método .clean de la clase padre
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        # Verificamos que las constraseñas coincidan.
        if password != password_confirmation:
            # En caso de ser distintas devolvemos un mensaje de error al html.
            raise forms.ValidationError('Passwords do not match.')

        # siempre debemos retornar el data
        return data

    # Creamos una instancia de User y Profile.
    def save(self):
        """
        save method.
        """
        data = self.cleaned_data
        data.pop('password_confirmation')

        # creamos el objeto user
        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()

class ProfileForm(forms.Form):

  website = forms.URLField(max_length=200, required=True)
  biography = forms.CharField(max_length=500, required=False)
  phone_number = forms.CharField(max_length=20, required=False)
  picture = forms.ImageField()