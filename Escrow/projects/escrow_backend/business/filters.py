from django_filters import rest_framework as filters
from .models import Order

class OrderFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    order_status = filters.CharFilter(field_name='order_status')

    class Meta:
        model = Order
        fields = ['created_at', 'order_status']
