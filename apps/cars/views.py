from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import F, Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import View
from apps.dealers.models import Dealer
from apps.cars.forms import CarForm, CarSwapForm
from apps.wallet.models import Wallet, WalletTransactions
from benny_dealz.utils import get_car_brands, get_states_only, get_car_logo, get_states
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from apps.cars.models import Car, CarSwap, Comment, Favorite, CarMedia
from ..common.views import convert_to_true_or_false_v2


class CarListView(ListView):
    paginate_by = 6
    template_name = 'cars/car_list.html'

    def get(self, request, *args, **kwargs):
        cars = Car.objects.filter(status='Available')
        total_cars = cars.count()
        top_brands = Car.objects.filter(status='Available').values('brand', 'brand_logo').annotate(total_cars=Count('id')).order_by('-total_cars')[:6]
        file_path = "benny_dealz/json_files/countries_states_cities.json"
        states = get_states(file_path, "Nigeria")
        states_with_count = []
        for state in states:
            cars_count = Car.objects.filter(dealer__addresses__state=state, status='Available').count()
            states_with_count.append({
                "state": state,
                "cars_count": cars_count
            })
        context = {
            "states": states_with_count,
            'cars': cars,
            'total_cars': total_cars,
            "top_brands": top_brands,
        }
        return render(request, self.template_name, context)


class CarDetailView(DetailView):
    model = Car
    context_object_name = "car"
    template_name = 'cars/car_detail.html'

    def get(self, request, *args, **kwargs):
        # Increment the view_count when a user accesses the details page
        self.object = self.get_object()
        self.object.view_count += 1
        self.object.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CarDetailView, self).get_context_data(**kwargs)
        context['similar_cars'] = Car.objects.filter(body_type=self.object.body_type).filter(
            condition=self.object.condition).exclude(pk=self.object.pk)[:4]
        return context

    def post(self, request, slug):
        message = request.POST["message"]
        context = self.get_context_data(object=self.get_object())
        comment = Comment.objects.create(
            car=self.get_object(),
            by=request.user,
            content=message
        )
        comment.save()
        messages.success(request, "Comment sent successfully")
        return render(request, self.template_name, context=context)


class CarCreateView(LoginRequiredMixin, View):
    template_name = "cars/car_form.html"
    upload_price = 500

    def get(self, request, *args, **kwargs):
        car_form = CarForm()
        dealer = Dealer.objects.get(user=self.request.user)
        # Get countries
        state_file_path = "benny_dealz/json_files/states-and-cities.json"
        states = get_states_only(state_file_path)
        # Get models
        brand_file_path = "benny_dealz/json_files/car-list.json"
        brands = get_car_brands(brand_file_path)
        context = {
            'form': car_form,
            'states': states,
            'models': brands,
            'dealer': dealer,
            'upload_price': self.upload_price,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        car_form = CarForm(request.POST, request.FILES)
        dealer = Dealer.objects.get(user=self.request.user)
        brand = request.POST.get("car_brand")
        model = request.POST.get("car_model")
        my_files = self.request.FILES.getlist("file")
        print(f"""
            brand: {brand}
            model: {model}
            my_files: {my_files}
        """)
        if car_form.is_valid():
            car = car_form.save(commit=False)
            car.dealer = dealer
            self.save_car(car, my_files, brand, model)
            messages.success(request, "Car uploaded successfully...")
            return redirect('dealers:dealer_car_list')
        context = {
            'form': car_form,
        }
        messages.warning(request, "Car upload failed check your wallet balance and try again...")
        return render(request, self.template_name, context)

    def save_car(self, car, my_files, brand, model):
        car.main_image = my_files[0]
        print(f"{my_files[0]} Saved successfully")
        file_path = "benny_dealz/json_files/car-list.json"
        del my_files[0]
        car.brand = brand
        car.model = model
        car.brand_logo = get_car_logo(file_path, brand)
        print(f"brand_logo: {car.brand_logo}")
        car.save()
        for media in my_files:
            img_doc = CarMedia.objects.create(
                car=car,
                image=media,
                uploaded_by=self.request.user
            )
            img_doc.save()


class CarUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        selected_id = request.GET.get("selected_id")
        print(f"""
            selected_id: {selected_id}
        """)
        car = Car.objects.get(id=selected_id)
        return JsonResponse({
            "id": car.id,
            "status": car.status,
            "can_be_swapped": car.can_be_swapped,
        })

    def post(self, request):
        selected_id = request.POST.get("selected_id")
        print(f"""
            selected_id: {selected_id}
        """)
        status = request.POST.get("status")
        can_be_swapped = convert_to_true_or_false_v2(request, "can_be_swapped")
        car = Car.objects.get(id=selected_id)
        car.status = status
        car.can_be_swapped = can_be_swapped
        car.save()
        return JsonResponse({
            "status": "success",
            "message": "Successfully updated the status..."
        })


class CarDeleteView(LoginRequiredMixin, DeleteView):

    def post(self, request):
        dealer = Dealer.objects.get(user=request.user)
        selected_id = request.POST.get('selectedID')
        print(selected_id)
        if selected_id:
            Car.objects.get(id=selected_id, dealer=dealer).delete()
            return JsonResponse({
                "status": "success",
                "message": "Deleted successfully..."
            })
        return JsonResponse({
            "status": "warning",
            "message": "Network error."
        })


class CarSwapListView(LoginRequiredMixin, ListView):
    model = CarSwap
    paginate_by = 6
    template_name = 'cars/swap_list.html'
    context_object_name = 'carswaps'


class CarSwapCreateView(LoginRequiredMixin, View):
    template_name = "cars/car_swap_form.html"

    def get(self, request, *args, **kwargs):
        # Get models
        brand_file_path = "benny_dealz/json_files/car-list.json"
        brands = get_car_brands(brand_file_path)
        context = {
            "form": CarSwapForm(),
            'models': brands,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        brand = request.POST.get("car_brand")
        model = request.POST.get("car_model")
        model_year = request.POST.get("model_year")
        body_type = request.POST.get("body_type")
        status = request.POST.get("status")
        price = request.POST.get("price")
        condition = request.POST.get("condition")
        transmission = request.POST.get("transmission")
        image = request.FILES.get("image")
        current_user = self.request.user
        print(f"""
            brand: {brand}
            model: {model}
            model_year: {model_year}
            body_type: {body_type}
            status: {status}
            price: {price}
            condition: {condition}
            transmission: {transmission}
            image: {image}
        """)
        # try:
        car_swap = CarSwap(
            brand=brand,
            model=model,
            model_year=model_year,
            body_type=body_type,
            status=status,
            price=price or 0.00,
            condition=condition,
            transmission=transmission,
            image=image,
            owner=current_user
        )
        car_swap.save()
        print("car swap saved successfully...")
        return JsonResponse({
            "status": "success",
            "message": "Submitted successfully..."
        })
        # except (Exception, IntegrityError) as e:
        #     return JsonResponse({
        #         "status": "info",
        #         "message": "Your request was already submitted successfully..."
        #     })


class CarSwapEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cars/swap_edit.html')

    def post(self, request, *args, **kwargs):
        _message = request.POST['message']
        subject = request.POST['subject']
        context = {'message': _message, 'subject': subject, 'name': self.request.user.username}
        email_template = render_to_string('support_email.html', context)
        try:
            send_mail = EmailMessage(
                'Car-Swap-Edit message for bennydealz.com.ng',
                email_template,
                self.request.user.email,
                [settings.SUPPORT_EMAIL],
            )
            send_mail.fail_silently = False
            send_mail.send()
            messages.success(request, "Email sent successfully...")
            return render(request, 'cars/swap_edit.html')
        except Exception:
            messages.warning(request, "Unable to send email please check your network")
            return render(request, 'cars/swap_edit.html')


class CarSwapDeleteView(LoginRequiredMixin, View):
    def get(self, request, slug, *args, **kwargs):
        user = self.request.user
        car_swap = CarSwap.objects.filter(slug=slug, owner=user)
        # user.swap_car.remove(car_swap)
        car_swap.delete()
        messages.success(request, "Your car deleted successfully successfully...")
        next_page = request.POST.get('next', '/')
        return HttpResponseRedirect(next_page)


class FavouriteCars(LoginRequiredMixin, View):

    def get(self, request):
        cars = request.user.favorite_cars.all()
        context = {
            "cars": cars
        }
        return render(request, 'cars/car_favourite.html', context)


class ToggleFavoriteView(LoginRequiredMixin, View):

    def post(self, request, car_id):
        user = request.user
        car = Car.objects.get(id=car_id)
        favorite = Favorite.objects.filter(user=user, car=car)
        if not favorite.exists():
            Favorite.objects.create(user=user, car=car)
            return JsonResponse({
                "status": "success",
                "message": "Car added to favorites",
                'is_favorite': True,  # Send the favorite ID back to the frontend
            })
        else:
            favorite.delete()
            return JsonResponse({
                "status": "error",
                "message": "Removed from favorite",
                'is_favorite': False,
            })


class RemoveFavoriteView(LoginRequiredMixin, View):

    def post(self, request, car_id):
        user = request.user
        car = Car.objects.get(id=car_id)
        favorite = Favorite.objects.filter(user=user, car=car).first()
        if favorite.user != user:
            return JsonResponse({
                "status": "error",
                "message": "You don't have permission to remove this favorite"
            })
        favorite.delete()
        return JsonResponse({
            "status": "success",
            "message": "Car removed from favorites"
        })


# ============== Other Car Features ================
class CarFeatureUpgrade(View):
    def get(self, request, slug):
        current_dealer = Dealer.objects.get(name=self.request.user)
        car = get_object_or_404(Car, slug=slug)
        wallet = Wallet.objects.get(dealer=current_dealer)
        if car.is_featured:
            expired_time = (datetime.now() + timedelta(hours=1))
            if datetime.now() == expired_time:
                self._extracted_from_get_14(
                    False,
                    car,
                    request,
                    "Car is no longer featured as its 24hrs due.",
                )
                return redirect('accounts:profile', self.request.user.slug)
        else:
            featured_price = 500
            if wallet.balance > featured_price:
                return self._extracted_from_get_23(featured_price, wallet, car, request)
        messages.error(request, "Balance is low fund your wallet...")
        return redirect("wallet:fund_wallet", wallet.uid)

    # TODO Rename this here and in `get`
    def _extracted_from_get_23(self, featured_price, wallet, car, request):
        wallet.balance = F('balance') - featured_price
        wallet.save()
        self._extracted_from_get_14(
            True, car, request, "Your car is now featured for 24hrs."
        )
        wallet_transaction = WalletTransactions(
            wallet=wallet,
            transaction_id=wallet.virtual_account_ref,
            currency=wallet.currency,
            amount=float(featured_price),
            payment_status="successful",
        )
        wallet_transaction.save()
        return redirect('accounts:profile', self.request.user.slug)

    # TODO Rename this here and in `get`
    def _extracted_from_get_14(self, arg0, car, request, arg3):
                # Delete session variable...
                # if 'time_left' in request.session:
                #     del request.session['time_left']

                # deactivate car featured...
        car.is_featured = arg0
        car.save(update_fields=['is_featured'])
        messages.success(request, arg3)


class CarFilterView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        global inspected_count, not_inspected_count, price_ranges, transmission_counts, fuel_type_counts
        file_path = "benny_dealz/json_files/countries_states_cities.json"
        states = get_states(file_path, "Nigeria")

        data_for_frontend = []

        for state in states:
            state_data = {
                "state": state,
                "cars_count": Car.objects.filter(dealer__addresses__state=state, status='Available').count(),
                "brands": [],
                "inspected": 0,
                "not_inspected": 0,
                "price_ranges": [],
                "transmissions": {},
                "fuel_type": {}
            }
            brands_for_state = Car.objects.filter(dealer__addresses__state=state, status='Available').values('brand').annotate(total_cars=Count('id'))
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
        brand = request.POST.get('brand')
        state = request.POST.get('state', '')
        car_brand = request.POST.get('car_brand', '')
        inspected = request.POST.get('inspected', '')
        price_range = request.POST.get('price', '')
        transmission = request.POST.getlist('transmission', [])
        fuel_type = request.POST.getlist('fuel_type', [])

        print(f"""
            brand: {brand}
            state: {state}
            car_brand: {car_brand}
            inspected: {inspected}
            price_range: {price_range}
            transmission: {transmission}
            fuel_type: {fuel_type}
        """)

        # Filter cars based on the received parameters
        filtered_cars = Car.objects.filter(status='Available')

        if state:
            filtered_cars = filtered_cars.filter(dealer__addresses__state=state)

        if car_brand:
            filtered_cars = filtered_cars.filter(brand=car_brand)

        if brand:
            filtered_cars = filtered_cars.filter(brand=brand)

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

        print(f"filtered_cars: {filtered_cars}")

        data_for_frontend = {
            "filtered_cars": [
                {
                    "slug": car.slug,
                    "status": car.status,
                    "get_main_image": car.get_main_image,
                    "favorited_by": request.user in car.favorited_by.all(),
                    "get_car_name": car.get_car_name,
                    "transmission": car.transmission,
                    "power": car.power,
                    "model_year": car.model_year,
                    "fuel": car.fuel,
                    "price": car.price,
                }
                for car in filtered_cars
            ]
        }
        return JsonResponse(data_for_frontend)
