import django_filters
from .models import TravelRequest, TravelEntry
from django.db.models import Q
from datetime import datetime

class TravelRequestFilter(django_filters.FilterSet):
    booking_date = django_filters.DateFilter(field_name='booking_date', lookup_expr='exact')
    booked_by = django_filters.CharFilter(field_name='booked_by', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # Nested entry filtering
    travel_mode = django_filters.CharFilter(method='filter_travel_mode')
    billing = django_filters.CharFilter(method='filter_billing')
    month_year = django_filters.CharFilter(method='filter_month_year')

    class Meta:
        model = TravelRequest
        fields = ['booking_date', 'booked_by', 'name', 'travel_mode', 'billing']

    def filter_travel_mode(self, queryset, name, value):
        return queryset.filter(entries__travel_mode__icontains=value, entries__is_delete=False).distinct()

    def filter_billing(self, queryset, name, value):
        return queryset.filter(entries__billing__icontains=value, entries__is_delete=False).distinct()
    
    def filter_month_year(self, queryset, name, value):
        try:
            # Expected format: "January-2025"
            date_obj = datetime.strptime(value, '%B-%Y')
            return queryset.filter(
                booking_date__year=date_obj.year,
                booking_date__month=date_obj.month
            )
        except ValueError:
            return queryset  # If format is invalid, return unfiltered queryset
