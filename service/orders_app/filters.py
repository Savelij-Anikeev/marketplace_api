from django_filters import rest_framework as filters

from .models import Order


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class OrderFilter(filters.FilterSet):
    user_id = filters.BaseInFilter(field_name='user_id')
    is_paid = filters.BooleanFilter(field_name='is_paid')
    cost = filters.BaseRangeFilter(field_name='cost')

    class Meta:
        model = Order
        fields = ['user_id', 'is_paid', 'cost']
