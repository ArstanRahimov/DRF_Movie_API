from rest_framework import serializers

from .models import Movie, Review


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""

    class Meta:
        model = Review
        fields = ('email', 'name', 'text', 'parent')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полное описание фильма"""

    """Переопределяем поля, для того, чтобы вместо id полей, выводились их названия(по полю 'name')"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    """По related_name = 'reviews' выводим отзывы к фильму"""
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft', )
