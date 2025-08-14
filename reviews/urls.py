# reviews/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("movies/<int:pk>/review/", views.add_review, name="add_review"),
    path("signup/", views.signup, name="signup"),
]
