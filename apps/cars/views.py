from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import View
from apps.dealers.models import Dealer
from apps.cars.forms import CarForm, CarSwapForm
from apps.wallet.models import Wallet, WalletTransactions
from benny_dealz.utils import get_car_brands, get_states_only, get_car_logo
from .filters import CarFilter
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from apps.cars.models import Car, CarSwap, Comment, Favorite, CarMedia
from ..common.views import convert_to_true_or_false_v2


class CarListView(ListView):
    paginate_by = 6
    template_name = 'cars/car_list.html'

    def get(self, request, *args, **kwargs):
        cars = Car.objects.all().exclude(status="Sold")
        total_cars = cars.count()
        my_car_filter = CarFilter(request.GET, queryset=cars)
        all_cars = my_car_filter.qs
        cars = my_car_filter.qs

        context = {
            'my_car_filter': my_car_filter,
            'cars': cars,
            'total_cars': total_cars,
            'all_cars': all_cars,
        }
        return render(request, self.template_name, context)


class CarDetailView(DetailView):
    model = Car
    context_object_name = "car"
    template_name = 'cars/test.html'

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
        car.manufacturer = brand
        car.make = model
        car.manufacturer_logo = get_car_logo(file_path, brand)
        print(f"manufacturer_logo: {car.manufacturer_logo}")
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
            manufacturer=brand,
            make=model,
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


# class AddFavoriteView(LoginRequiredMixin, View):
#     def post(self, request, car_id):
#         user = request.user
#         car = Car.objects.get(id=car_id)
#         favorite = Favorite.objects.filter(user=user, car=car)
#         if not favorite.exists():
#             Favorite.objects.create(user=user, car=car)
#             return JsonResponse({
#                 "status": "success",
#                 "message": "Car added to favorites",
#                 'is_favorite': True,  # Send the favorite ID back to the frontend
#             })
#         else:
#             favorite.delete()
#             return JsonResponse({
#                 "status": "error",
#                 "message": "Removed from favorite",
#                 'is_favorite': False,
#             })


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
class CarFeatureUpgrade(LoginRequiredMixin, View):
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


# class CarCreateView(LoginRequiredMixin, View):
#     template_name = "cars/car_form.html"
#
#     def get(self, request, *args, **kwargs):
#         car_form = CarForm()
#         dealer = Dealer.objects.get(user=self.request.user)
#         wallet = Wallet.objects.get(dealer=dealer)
#         upload_price = 3000
#         context = {
#             'form': car_form,
#             'wallet': wallet,
#             'upload_price': upload_price,
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         car_form = CarForm(request.POST, request.FILES)
#         get_current_dealer = Dealer.objects.get(name=self.request.user)
#         wallet = Wallet.objects.get(dealer=get_current_dealer)
#         upload_price = 3000
#         if wallet.balance > upload_price:
#             if car_form.is_valid():
#                 current_car = car_form.save(commit=False)
#                 current_car.dealer = get_current_dealer
#                 wallet.balance = F('balance') - upload_price
#                 wallet.save()
#                 current_car.save()
#                 messages.success(request, "Car uploaded successfully...")
#                 # Update user wallet transaction
#                 wallet_transaction = WalletTransactions(
#                     wallet=wallet,
#                     transaction_id=wallet.virtual_account_ref,
#                     currency=wallet.currency,
#                     amount=float(upload_price),
#                     payment_status="successful",
#                 )
#                 wallet_transaction.save()
#                 print("Transaction success wallet transactions updated")
#                 return redirect('accounts:profile', self.request.user.slug)
#         else:
#             wallet_transaction = WalletTransactions(
#                 wallet=wallet,
#                 transaction_id=wallet.virtual_account_ref,
#                 currency=wallet.currency,
#                 amount=float(upload_price),
#                 payment_status="failed",
#             )
#             wallet_transaction.save()
#             print("Transaction failed wallet transactions updated")
#             messages.error(request, "Balance is low fund your wallet to upload cars.")
#             return redirect("wallet:fund_wallet", wallet.uid)
#
#         context = {
#             'form': car_form,
#             'wallet': wallet,
#             'upload_price': upload_price,
#         }
#         messages.warning(request, "Car upload failed check your wallet balance and try again...")
#         return render(request, self.template_name, context)
#
