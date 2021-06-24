from django_filters import CharFilter
from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    name = CharFilter(lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('year',)
