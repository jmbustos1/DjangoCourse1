# users/urls.py

"""Users URLs."""

# Django
from django.urls import path
from django.views.generic import TemplateView

# View
from users import views


urlpatterns = [

    # Posts
    path(
        route='detail/<str:username>/',
        view=TemplateView.as_view(template_name='users/detail.html'),
        name='detail'
    ),

    # Management
    path(
        route='login/',
        view=views.login_view,
        name='login'
    ),
    path(
        route='logout/',
        view=views.logout_view,
        name='logout'
    ),
    path(
        route='signup/',
        view=views.signup,
        name='signup'
    ),
    path(
        route='me/profile/',
        view=views.UpdateProfileView.as_view(template_name='users/update_profile.html'),
        name='update_profile'
    )

]