import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    in_stock = django_filters.BooleanFilter(field_name='stock_quantity', lookup_expr='gte', method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['name', 'category', 'min_price', 'max_price', 'in_stock']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gte=1)
        else:
            return queryset.filter(stock_quantity__lt=1)