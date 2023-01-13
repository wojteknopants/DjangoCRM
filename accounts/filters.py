import django_filters
from django_filters import DateFilter, CharFilter, DateFromToRangeFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    dates = DateFromToRangeFilter(field_name = "date_created")
    note = CharFilter(field_name="note", lookup_expr="icontains")
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']