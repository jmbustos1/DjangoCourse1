# posts/urls.py

"""Posts URLs."""

# Django
from django.urls import path

# Views
from goodapp import views

urlpatterns = [

    path(
        route='',
        view=views.PostsFeedView.as_view(),
        name='feed'
    ),

    path(
        route='posts/new/',
        view=views.create_post,
        name='create'
    ),
]