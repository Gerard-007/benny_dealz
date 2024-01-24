import django_filters
from .models import Car
from apps.cars.car_utils import MANUFACTURERS, STATUS, YEAR_CHOICES, CATEGORY, BODY_TYPE, TRANSMISSION, FUEL_TYPE


class CarFilter(django_filters.FilterSet):
    make = django_filters.CharFilter(lookup_expr='icontains')
    # manufacturer = django_filters.ModelChoiceFilter(choices=MANUFACTURERS, null_label='Any', null_value='')
    # transmission = django_filters.ModelChoiceFilter(choices=TRANSMISSION, null_label='Any', null_value='')
    # status = django_filters.ModelChoiceFilter(choices=STATUS, null_label='Any', null_value='')
    # condition = django_filters.ModelChoiceFilter(choices=CATEGORY, null_label='Any', null_value='')
    # body_type = django_filters.ModelChoiceFilter(choices=BODY_TYPE, null_label='Any', null_value='')
    # fuel = django_filters.ModelChoiceFilter(choices=FUEL_TYPE, null_label='Any', null_value='')
    year_gt = django_filters.NumberFilter(field_name='model_year', lookup_expr='gt')
    year_lt = django_filters.NumberFilter(field_name='model_year', lookup_expr='lt')
    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    mileage_gt = django_filters.NumberFilter(field_name='mileage', lookup_expr='gt')
    mileage_lt = django_filters.NumberFilter(field_name='mileage', lookup_expr='lt')

    class Meta:
        model = Car
        fields = [
            'model_year',
            'manufacturer',
            'status',
            'condition',
            'body_type',
            'mileage',
            'fuel',
        ]
