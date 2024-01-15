from django_filters import rest_framework as filters

from product_app.models import Product


class ProductFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    categories = ProductFilterInFilter(field_name='categories__name', lookup_expr='in')
    vendor = ProductFilterInFilter(field_name='vendor__name', lookup_expr='in')
    rating = filters.RangeFilter()
    vendor_rating = filters.RangeFilter(field_name='vendor__rating')

    class Meta:
        model = Product
        fields = ('categories', 'rating', 'vendor')
