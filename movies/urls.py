from django.urls import path

from .views import MovieListView, MovieDetailView, ReviewCreateView

urlpatterns = [
    path('movies/', MovieListView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('reviews/', ReviewCreateView.as_view()),
]

