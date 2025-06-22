import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    date_min = django_filters.DateFilter(field_name="timestamp", lookup_expr='gte')
    date_max = django_filters.DateFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'date_min', 'date_max']
