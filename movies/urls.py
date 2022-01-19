from django.urls import path

from .views import (MovieListView, MovieDetailView, ReviewCreateView,
                    AddStarRatingView, ActorsListView, ActorDetailView)

urlpatterns = [
    path('movies/', MovieListView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('reviews/', ReviewCreateView.as_view()),
    path('rating/', AddStarRatingView.as_view()),
    path('actors/', ActorsListView.as_view()),
    path('actors/<int:pk>/', ActorDetailView.as_view()),
]

