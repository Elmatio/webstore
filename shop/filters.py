import django_filters
from django.db.models import Q
from .models import Product
import re


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')
    color = django_filters.CharFilter(method='filter_by_color', label='Цвет')
    manufacturer = django_filters.CharFilter(field_name='description', lookup_expr='icontains', label='Производитель')
    material = django_filters.CharFilter(method='filter_by_material', label='Материал')
    country = django_filters.CharFilter(method='filter_by_country', label='Страна производитель')
    length = django_filters.NumberFilter(method='filter_by_length', label='Длина')
    width = django_filters.NumberFilter(method='filter_by_width', label='Ширина')

    class Meta:
        model = Product
        fields = []

    def filter_by_color(self, queryset, name, value):
        return queryset.filter(Q(name__iregex=value) | Q(description__iregex=f'Цвет: {value}'))

    def filter_by_material(self, queryset, name, value):
        return queryset.filter(Q(name__iregex=value) | Q(description__iregex=f'Материал: {value}'))

    def filter_by_country(self, queryset, name, value):
        return queryset.filter(Q(name__iregex=value) | Q(description__iregex=f'Страна-производитель: {value}'))

    def filter_by_length(self, queryset, name, value):
        return queryset.filter(Q(name__iregex=value) | Q(description__iregex=f'Длина (см): {value}'))

    def filter_by_width(self, queryset, name, value):
        return queryset.filter(Q(name__iregex=value) | Q(description__iregex=f'Ширина (см): {value}'))
