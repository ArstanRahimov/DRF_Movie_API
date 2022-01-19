from rest_framework import generics
from django.db import models

from .models import Movie, Actor
from .serializers import (MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
                          CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer)
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
     """Вывод списка фильмов"""

     serializer_class = MovieListSerializer

# rating_user будет автоматически добавлено каждому объекту Movie и ему будет присвоено значение True/False
# в зависимости от того, ставил ли он рейтинг фильму

     def get_queryset(self):
         movies = Movie.objects.filter(draft=False).annotate(
             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
         ).annotate(
             average_rating=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
         )  # общую сумму звезд рейтинга делим на количество записей с оценками. Метод F позволяет производить мат.
         # операции
         return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод полного описания фильма"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""

    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""

    serializer_class = CreateRatingSerializer

    # метод для переопределения сохранения данных сериализатора
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод полного описания актера или режиссера"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
