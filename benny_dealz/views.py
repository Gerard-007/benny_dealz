import datetime
import re

from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from validate_email import validate_email
from apps.accounts.models import User
from apps.cars.car_utils import body_types
from apps.dealers.models import Dealer
from apps.profiles.models import Profile
from benny_dealz import settings
from benny_dealz.utils import get_states, get_cities_only, get_car_brands, get_car_brand_models, get_cities_only_v2
from apps.cars.models import Car


class HomeView(View):
    template_name = "index.html"

    def get(self, request):
        latest_cars = Car.objects.all().order_by("-date")[:6]
        dealers_in_same_state = Dealer.objects.filter(
            user__profile__state=request.user.profile.state) if request.user.is_authenticated else None
        top_brands = Car.objects.values('brand', 'brand_logo').annotate(total_cars=Count('id')).order_by('-total_cars')[:6]
        # Get models
        brand_file_path = "benny_dealz/json_files/car-list.json"
        brands = get_car_brands(brand_file_path)
        context = {
            "brands": brands,
            "body_types": body_types,
            "years": list(range(1995, datetime.date.today().year)),
            "cars": latest_cars,
            "dealers": dealers_in_same_state,
            "top_brands": top_brands,
        }
        return render(request, self.template_name, context)


class FilterCarView(View):
    def get(self, request, *args, **kwargs):
        file_path = "benny_dealz/json_files/countries_states_cities.json"
        states = get_states(file_path, "Nigeria")
        context = {
            "states": states,
        }

    def post(self, request):
        condition = request.POST.get('condition')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year')
        mileage = request.POST.get('mileage')
        price = request.POST.get('price')
        body_type = request.POST.get('body_type')

        print(f"""
            condition: {condition}
            brand: {brand}
            model: {model}
            year: {year}
            mileage: {mileage}
            price: {price}
            body_type: {body_type}
        """)

        price_min = 0.00
        price_max = 0.00

        milage_min = 0.00
        milage_max = 0.00

        if price:
            prices = price.split(',')
            price_min = int(prices[0])
            price_max = int(prices[1])

        if mileage:
            milages = mileage.split(',')
            milage_min = int(milages[0])
            milage_max = int(milages[1])

        # Construct the filter parameters
        filters = {}
        if condition:
            filters['condition'] = condition
        if brand:
            filters['brand'] = brand
        if model:
            filters['model'] = model
        if year:
            filters['model_year'] = year
        if milage_min and milage_max:
            filters['mileage__range'] = (milage_min, milage_max)
        if price_min and price_max:
            filters['price__range'] = (price_min, price_max)
        if body_type:
            filters['body_type'] = body_type

        # Apply filters to the Car model
        filtered_cars = Car.objects.filter(**filters)

        # Convert queryset to a list of dictionaries
        cars_list = list(filtered_cars.values())

        # Redirect to the search.html page with filtered results
        return render(request, 'pages/search.html', {'cars': cars_list})
        # return JsonResponse({'cars': cars_list})


class AboutUs(View):
    template_name = "pages/about.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class ContactUs(View):
    template_name = "pages/contact.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        email_template = render_to_string(
            'includes/contact_email.html',
            {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
            }
        )
        emailSubject = f"Benny Dealz contact message from {name}"
        send_email = EmailMultiAlternatives(
            subject=emailSubject,
            body=emailSubject,
            from_email=settings.SUPPORT_EMAIL,
            to=["geetechlab@gmail.com", "dealzbenny@gmail.com", settings.SUPPORT_EMAIL],
            headers={'Reply-To': email, 'format': 'flowed'}
        )
        send_email.attach_alternative(email_template, "text/html")
        try:
            send_email.send(fail_silently=False)
            print(f"Email sent to {email}")
            return JsonResponse({
                "status": "success",
                "message": "Message was sent successfully"
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                "status": "error",
                "message": "Email network error"
            })


class GetStates(View):

    def post(self, request):
        file_path = "benny_dealz/json_files/countries_states_cities.json"
        country = request.POST['country']
        states = get_states(file_path, country)
        data = {
            "states": states,
            "message": "request was successful states populated..."
        }
        return JsonResponse(data=data, safe=False)


class GetCities(View):

    def post(self, request):
        country = request.POST.get('country')
        state = request.POST['state']
        if country == "" or country is None:
            file_path = "benny_dealz/json_files/states-and-cities.json"
            cities = get_cities_only_v2(file_path, state)
        else:
            file_path = "benny_dealz/json_files/countries_states_cities.json"
            cities = get_cities_only(file_path, country, state)
        data = {
            "cities": cities,
            "success": "request was successful cities populated..."
        }
        return JsonResponse(data=data, safe=False)


class GetCarBrands(View):
    def post(self, request):
        file_path = "benny_dealz/json_files/car-list.json"
        brands = get_car_brands(file_path)
        data = {
            "brands": brands,
            "message": "request was successful brands populated..."
        }
        return JsonResponse(data=data, safe=False)


class GetCarModels(View):

    def post(self, request):
        file_path = "benny_dealz/json_files/car-list.json"
        brand = request.POST['brand']
        # print(f"brand: {brand}")
        models = get_car_brand_models(file_path, brand)
        data = {
            "models": models,
            "message": "request was successful brands populated..."
        }
        return JsonResponse(data=data, safe=False)


def check_username(request):
    username = request.POST.get('username')
    if not str(username).isalnum():
        return HttpResponse("<small class='text-warning'>Username should contain alphanumeric characters.</small>")
    if User.objects.filter(username=username).exists():
        return HttpResponse("<small class='text-danger'>Sorry username already in use.</small>")
    return HttpResponse("<small class='text-success'>Username is available.</small>")


def check_email(request):
    email = request.POST.get('email')
    if not validate_email(email):
        return HttpResponse("<small class='text-warning'>Wrong email address.</small>")
    if User.objects.filter(email=email).exists():
        return HttpResponse("<small class='text-danger'>Sorry email already in use.</small>")
    return HttpResponse("<small class='text-success'>Email is available.</small>")


def check_password(request):
    password = request.POST.get('password')
    # Check if the password is empty or has fewer than 6 characters
    if not password or len(password) < 6:
        return HttpResponse("<small class='text-danger'>Password is short, must be at least 6 characters</small>")
    # Check if the password contains at least one uppercase letter, one lowercase letter, and one digit
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
        return HttpResponse(
            "<small class='text-warning'>Password must contain at least one uppercase letter, one lowercase letter, and one digit</small>")
    # Password is valid
    return HttpResponse("<small class='text-success'>Password is valid</small>")


def confirm_password(request):
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    if password == "" and password2 == "":
        return HttpResponse("<small class='text-warning'>Passwords are empty</small>")
    elif password == password2:
        return HttpResponse("<small class='text-success'>Passwords matched and OK!</small>")
    return HttpResponse("<small class='text-danger'>Password does not matched!!!</small>")


def check_phone(request):
    phone_number = request.POST.get('phone')
    print(f"Checking Phone {phone_number}")
    if "+" not in phone_number:
        return HttpResponse(
            "<small class='text-danger'>Please affix country code on your phone number eg(+2348031234567)</small>")
    elif len(phone_number) > 14 or len(phone_number) < 14:
        return HttpResponse("<small class='text-danger'>Invalid phone number</small>")
    elif Profile.objects.filter(phone_number=phone_number).exists():
        return HttpResponse("<small class='text-danger'>Sorry phone number already in use.</small>")
    return HttpResponse("<small class='text-success'>Phone number is available.</small>")


def check_business_phone(request):
    phone_number = request.POST.get('business_phone')
    print(f"Checking Phone {phone_number}")
    if "+" not in phone_number:
        return HttpResponse(
            "<small class='text-danger'>Please affix country code on your phone number eg(+2348031234567)</small>")
    if len(phone_number) > 14 or len(phone_number) < 14:
        return HttpResponse("<small class='text-info'>Invalid phone number</small>")
    if Dealer.objects.filter(business_phone=phone_number).exists() or Profile.objects.filter(
            phone_number=phone_number).exists():
        return HttpResponse("<small class='text-danger'>Sorry phone number already in use.</small>")
    return HttpResponse("<small class='text-success'>Phone number is available.</small>")


def check_business_name(request):
    business_name = request.POST.get('business_name')
    if Dealer.objects.filter(business_name=business_name).exists():
        return HttpResponse("<small class='text-danger'>Sorry business name already in use.</small>")
    return HttpResponse("<small class='text-success'>Business name is available.</small>")


def check_business_email(request):
    business_email = request.POST.get('business_email')
    if not validate_email(business_email):
        return HttpResponse("<small class='text-warning'>Wrong email address.</small>")
    if Dealer.objects.filter(business_email=business_email).exists():
        return HttpResponse("<small class='text-danger'>Sorry email already in use.</small>")
    return HttpResponse("<small class='text-success'>Email is available.</small>")


# def log_messages(request):
#     if request.is_ajax() and request.method == "POST":
#         messages = [record.getMessage() for record in logging.getLogger().records]
#         return JsonResponse({
#             "messages": messages
#         })


# def log_messages(request):
#     if request.is_ajax() and request.method == "POST":
#         messages = []
#         for record in logging.getLogger().records:
#             messages.append(record.getMessage())
#         # Clear the logs
#         logging.getLogger().handlers[0].flush()
#         return JsonResponse({
#             "messages": messages
#         })
