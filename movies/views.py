from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db import models

from .models import Movie, Actor
from .serializers import (MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
                          CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer)
from .service import get_client_ip


class MovieListView(APIView):
     """Вывод списка фильмов"""

# rating_user будет автоматически добавлено каждому объекту Movie и ему будет присвоено значение True/False
# в зависимости от того, ставил ли он рейтинг фильму

     def get(self, request):
         movies = Movie.objects.filter(draft=False).annotate(
             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
         ).annotate(
             average_rating=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
         )  # общую сумму звезд рейтинга делим на количество записей с оценками. Метод F позволяет производить мат.
         # операции
         serializer = MovieListSerializer(movies, many=True)
         return Response(serializer.data)


class MovieDetailView(APIView):
    """Вывод полного описания фильма"""

    def get(self, request, pk):
        movies = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movies)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Добавление отзыва к фильму"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid(raise_exception=True):
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга фильму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод полного описания актера или режиссера"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
