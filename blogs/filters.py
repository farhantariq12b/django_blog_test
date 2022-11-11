import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class BlogFilter(django_filters.FilterSet):
    published_date = DateFilter(field_name='created_date', lookup_expr='gte')
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['category', 'id', 'created_date', 'content', 'user', 'image_url']