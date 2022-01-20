from django_filters import rest_framework as filters
from movies.models import Movie


def get_client_ip(request):
    """Получение IP пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """Так как Genres это Many2Many и нам нужно искать в диапозоне имен(боевики, комедии и тд), используем
    BaseInFilter. А так как ищем по названию, а не по id(в таблице указывается именно id, так как это Many2Many
    таблица), то используем CharFilter"""
    pass


class MovieFilter(filters.FilterSet):
    """наследуясь от FilterSet, мы можем указать поля и дополнительную логику, с помощью которой будем фильтровать"""
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')  # поле по которому ищем - genres__name,
    # lookup_expr='in' - указывает как нам нужно фильтровать это поле(in) (?genres=Боевик или
    # ?year_min=1984&genres=Боевик,Комедия)
    year = filters.RangeFilter()  # для поля year будет диапозон дат (?year_min=1984 или ?year_min=1984&year_max=2020)

    class Meta:
        """указываем модель, которую будем фильтровать и поля"""
        model = Movie
        fields = ('genres', 'year')
