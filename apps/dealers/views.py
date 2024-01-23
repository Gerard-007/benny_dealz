from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.views.generic.base import View
from apps.cars.models import Car
from apps.dealers.models import Dealer, DealerAddress
from benny_dealz.utils import get_states_only


class DealerListView(ListView):
    model = Dealer
    context_object_name = 'dealers'
    paginate_by = 6
    template_name = "dealers/dealer_list.html"

    def get_queryset(self):
        return super().get_queryset().annotate(total_cars=Count('cars'))


class DealerDashboardView(LoginRequiredMixin, View):
    template_name = "dealers/dashboard.html"

    def get(self, request):
        dealer = Dealer.objects.get(user=self.request.user)
        cars = Car.objects.filter(dealer=dealer)
        available_cars = cars.filter(status="Available").order_by("-date")[:6]
        total_view_counts = dealer.total_view_counts()
        context = {
            "available_car_count": available_cars.count(),
            "car_count": cars.count(),
            "cars": available_cars,
            "total_view_counts": total_view_counts
        }
        return render(request, self.template_name, context)


class DealerCarListView(LoginRequiredMixin, View):
    template_name = "dealers/dealer_car_list.html"

    def get(self, request):
        dealer = Dealer.objects.get(user=self.request.user)
        cars = Car.objects.filter(dealer=dealer)
        context = {
            "cars": cars,
        }
        return render(request, self.template_name, context)


class DealerDetailView(LoginRequiredMixin, DetailView):
    template_name = "dealers/dealer_detail.html"
    context_object_name = 'dealer'
    model = Dealer
    success_url = reverse_lazy('/')

    def get_object(self, queryset=None):
        return Dealer.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, *args, **kwargs):
        context = super(DealerDetailView, self).get_context_data()
        context['my_cars'] = Car.objects.filter(dealer=self.get_object())
        context['sold_cars'] = context['my_cars'].filter(status="Sold").count()
        context['available_cars'] = context['my_cars'].filter(status="Available").count()
        return context


class DealerCreateView(LoginRequiredMixin, View):

    def post(self, request):
        business_logo = request.FILES.get("image")
        business_name = request.POST.get("business_name")
        business_email = request.POST.get("business_email")
        business_phone = request.POST.get("business_phone")
        selected_id = request.POST.get("selected_id")
        print(f"""
            business_logo: {business_logo}
            business_name: {business_name}
            business_email: {business_email}
            business_phone: {business_phone}
            selected_id: {selected_id}
        """)
        if selected_id == "" or selected_id is None:
            dealer = Dealer.objects.create(
                user=self.request.user,
                business_name=business_name,
                business_email=business_email,
                business_phone=business_phone,
                business_logo=business_logo
            )
            # dealer.save()
            # now get the user and update is_a_dealer status...
            # user = User.objects.get(username=self.request.user.username)
            # user.is_a_dealer = True
            # user.save(update_fields=["is_a_dealer"])
            return JsonResponse({
                "status": "success",
                "message": "Dealer account created successfully..."
            })
        dealer = Dealer.objects.get(id=selected_id)
        dealer.business_phone = business_phone
        dealer.business_logo = business_logo
        dealer.save(update_fields=["business_phone", "business_logo"])
        return JsonResponse({
            "status": "success",
            "message": "Your dealership details was updated successfully..."
        })


class DealerUpdateView(LoginRequiredMixin, View):

    def post(self, request):
        business_logo = request.FILES.get("image")
        business_phone = request.POST.get("business_phone")
        dealer = Dealer.objects.get(
            user=self.request.user
        )
        dealer.business_phone = business_phone
        dealer.save(update_fields=["business_logo", "business_phone"])
        return JsonResponse({
            "status": "success",
            "message": "Your details were update successfully."
        })


class DealerAddressListView(LoginRequiredMixin, View):
    template_name = "dealers/dealer_address_create.html"

    def get(self, request):
        dealer = Dealer.objects.get(user=request.user)
        addresses = DealerAddress.objects.filter(dealer=dealer)
        state_file_path = "benny_dealz/json_files/states-and-cities.json"
        states = get_states_only(state_file_path)
        context = {
            "addresses": addresses,
            'states': states,
        }
        return render(request, self.template_name, context)


class DealerAddressCreateView(LoginRequiredMixin, View):

    def post(self, request):
        dealer = Dealer.objects.get(user=request.user)
        address_line_1 = request.POST.get("address_line_1")
        address_line_2 = request.POST.get("address_line_2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        postal_code = request.POST.get("postal_code")
        selected_id = request.POST.get('id')
        print(f"""
            selected_id: {selected_id}
            dealer: {dealer}
            address_line_1: {address_line_1}
            address_line_2: {address_line_2}
            city: {city}
            state: {state}
            country: {country}
            postal_code: {postal_code}
        """)
        if selected_id == "" or selected_id is None:
            try:
                address = DealerAddress(
                    dealer=dealer,
                    address_line_1=address_line_1,
                    address_line_2=address_line_2,
                    city=city,
                    state=state,
                    country=country,
                    postal_code=postal_code
                )
                address.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Address added successfully..."
                })
            except (IntegrityError, Exception) as e:
                return JsonResponse({
                    "status": "warning",
                    "message": "Input Error/Address already exists",
                })
        address = DealerAddress.objects.get(
            id=selected_id,
            dealer=dealer,
        )
        address.address_line_1 = address_line_1
        address.address_line_2 = address_line_2
        address.city = city
        address.state = state
        address.country = country
        address.postal_code = postal_code
        address.save()
        return JsonResponse({
            "status": "success",
            "message": "Address updated successfully..."
        })


class DealerAddressUpdateView(LoginRequiredMixin, View):

    def post(self, request):
        dealer = Dealer.objects.get(user=request.user)
        selected_id = request.POST.get('id')
        print(f"selected_id: {selected_id}")
        address = DealerAddress.objects.get(
            id=selected_id,
            dealer=dealer
        )
        return JsonResponse({
            "id": address.id,
            "address_line_1": address.address_line_1,
            "address_line_2": address.address_line_2,
            "city": address.city,
            "state": address.state,
            "country": address.country,
            "postal_code": address.postal_code,
        })


class DealerAddressDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        dealer = Dealer.objects.get(user=request.user)
        selected_id = request.POST.get('selectedID')
        print(selected_id)
        if selected_id:
            DealerAddress.objects.get(id=selected_id, dealer=dealer).delete()
            return JsonResponse({
                "status": "success",
                "message": "Deleted successfully..."
            })
        return JsonResponse({
            "status": "warning",
            "message": "Network error."
        })
