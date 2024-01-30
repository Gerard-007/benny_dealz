from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, Q

from apps.cars.models import Car
from benny_dealz.utils import get_states


class CarFilterView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        global inspected_count, not_inspected_count, price_ranges, transmission_counts, fuel_type_counts
        file_path = "benny_dealz/json_files/countries_states_cities.json"
        states = get_states(file_path, "Nigeria")

        data_for_frontend = []

        for state in states:
            state_data = {
                "state": state,
                "cars_count": Car.objects.filter(dealer__addresses__state=state).count(),
                "brands": [],
                "inspected": 0,
                "not_inspected": 0,
                "price_ranges": [],
                "transmissions": {},
                "fuel_type": {}
            }
            brands_for_state = Car.objects.filter(dealer__addresses__state=state).values('brand').annotate(total_cars=Count('id'))
            for brand in brands_for_state:
                state_data["brands"].append({
                    "brand": brand['brand'],
                    "cars_count": brand['total_cars']
                })
            data_for_frontend.append(state_data)

            # Get counts for other filters
            inspected_count = Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(car_inspection=True)).count()
            state_data["inspected"] = inspected_count

            not_inspected_count = Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(car_inspection=False)).count()
            print(f"inspected {state}: {inspected_count}")
            state_data["not_inspected"] = not_inspected_count

            # Append counts to lists
            state_data["price_ranges"].append({
                "range": "Below ₦1m",
                "count": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(price__lte=1000000)).count()
            })
            state_data["price_ranges"].append({
                "range": "₦1m - ₦2m",
                "count": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(price__range=(1000000, 2000000))).count()
            })
            state_data["price_ranges"].append({
                "range": "₦2m - ₦4m",
                "count": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(price__range=(2000000, 4000000))).count()
            })
            state_data["price_ranges"].append({
                "range": "₦4m - ₦6m",
                "count": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(price__range=(4000000, 6000000))).count()
            })
            state_data["price_ranges"].append({
                "range": "₦6m - ₦10m",
                "count": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(price__range=(6000000, 10000000))).count()
            })
            state_data["price_ranges"].append({
                "range": "More than ₦10m",
                "count": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(price__gt=10000000)).count()
            })

            state_data["transmissions"] = {
                "Automatic": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(transmission='Automatic')).count(),
                "Manual": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(transmission='Manual')).count(),
                "Duplex": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(transmission='Duplex')).count(),
            }

            state_data["fuel_type"] = {
                "Petrol": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(fuel='Petrol')).count(),
                "Diesel": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(fuel='Diesel')).count(),
                "CNG": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(fuel='CNG')).count(),
                "Hybrid": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(fuel='Hybrid')).count(),
                "Electric": Car.objects.filter(Q(dealer__addresses__state=state) & Q(status='Available') & Q(fuel='Electric')).count(),
            }

        return JsonResponse({
            "data": data_for_frontend
        })

    def post(self, request, **kwargs):
        # Get filter parameters from the POST request
        state = request.POST.get('state', '')
        car_brand = request.POST.get('car_brand', '')
        inspected = request.POST.get('inspected', '')
        price_range = request.POST.get('price', '')
        transmission = request.POST.getlist('transmission', [])
        fuel_type = request.POST.getlist('fuel_type', [])

        # Filter cars based on the received parameters
        filtered_cars = Car.objects.filter(status='Available')

        if state:
            filtered_cars = filtered_cars.filter(dealer__addresses__state=state)

        if car_brand:
            filtered_cars = filtered_cars.filter(brand=car_brand)

        if inspected == 'inspected':
            filtered_cars = filtered_cars.filter(car_inspection=True)

        elif inspected == 'not_inspected':
            filtered_cars = filtered_cars.filter(car_inspection=False)

        if price_range:
            min_price, max_price = map(int, price_range.split(','))
            filtered_cars = filtered_cars.filter(price__range=(min_price, max_price))

        if transmission:
            filtered_cars = filtered_cars.filter(transmission__in=transmission)

        if fuel_type:
            filtered_cars = filtered_cars.filter(fuel__in=fuel_type)

        # Prepare data to be sent to the frontend
        data_for_frontend = {
            "filtered_cars": [
                {"id": car.id, "brand": car.brand, "model": car.model}  # Add other fields as needed
                for car in filtered_cars
            ],
            "inspected_count": inspected_count,
            "not_inspected_count": not_inspected_count,
            # Add other counts as needed
        }

        return JsonResponse(data_for_frontend)