from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (MovieViewSet, ReviewCreateView,
                    AddStarRatingView, ActorViewSet)


router = DefaultRouter()
router.register('actors', ActorViewSet, basename='actors')
router.register('movies', MovieViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls)),
    # path('movies/<int:pk>/', MovieDetailView.as_view()),
    path('reviews/', ReviewCreateView.as_view()),
    path('rating/', AddStarRatingView.as_view()),
    # path('actors/', ActorsListView.as_view()),
    # path('actors/<int:pk>/', ActorDetailView.as_view()),
]

