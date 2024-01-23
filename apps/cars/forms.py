from django.forms import ModelForm
from apps.cars.models import Car, CarSwap


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = [
            # 'manufacturer',
            # 'make',
            # 'status',
            'model_year',
            'condition',
            'body_type',
            # 'main_image',
            'mileage',
            'transmission',
            'power',
            'engine_size',
            'number_of_cylinder',
            'number_of_seats',
            'fuel',
            'price',
            'description',
            'can_be_swapped',

            'coolBox',
            'sunroof',
            'DVDSystem',
            'remoteKey',
            'carTracker',
            'parkAssist',
            'heatedSeats',
            'parkingSensor',
            'pushStart',
            'reverseCamera',
            'navigationSystem',
            'bluetoothHandsFree',
            'audioSystem'
        ]


class CarSwapForm(ModelForm):
    class Meta:
        model = CarSwap
        fields = [
            'manufacturer',
            'make',
            'model_year',
            'body_type',
            'price',
            'status',
            'condition',
            'transmission',
            'image'
        ]
