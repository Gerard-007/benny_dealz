from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import DetailView, UpdateView
from apps.dealers.models import Dealer, DealerAddress
from apps.profiles.models import Profile
from benny_dealz.utils import get_states_only


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = "profiles/profile.html"

    def get_object(self, queryset=None):
        return Profile.objects.get(slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context["user"] = self.get_object().user
        context["today"] = datetime.now().date()
        # file_path = "benny_dealz/json_files/countries_states_cities.json"
        # context["countries"] = get_countries(file_path)
        state_file_path = "benny_dealz/json_files/states-and-cities.json"
        context["states"] = get_states_only(state_file_path)
        context["dealer"] = Dealer.objects.filter(user=self.get_object().user).first() if self.request.user.is_a_dealer else None
        return context


class GetProfileData(LoginRequiredMixin, View):

    def get(self, request, slug):
        profile = Profile.objects.get(slug=slug)
        data = {
            "gender": profile.gender,
            "birth_day": profile.birth_day,
            "bio": profile.bio,
            "image": str(profile.image_url),
            "state": profile.state,
            "city": profile.city,
            "local_area": profile.local_area,
            "address": profile.address,
        }
        return JsonResponse(data)


class ProfileUpdateView(LoginRequiredMixin, View):

    def post(self, request, slug):
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        state = request.POST.get("state")
        city = request.POST.get("city")
        local_area = request.POST.get("local_area")
        address = request.POST.get("address")
        print(f"""
            # Profile Data...
            full_name: {full_name}
            phone: {phone}
            gender: {gender}
            state: {state}
            city: {city}
            local_area: {local_area}
            address: {address}
        """)
        if profile := Profile.objects.filter(slug=slug).first():
            profile.full_name = full_name
            profile.phone_number = phone
            profile.gender = gender
            profile.state = state
            profile.city = city
            profile.local_area = local_area
            profile.address = address
            profile.save()
        if request.user.is_a_dealer:
            dealer = Dealer.objects.filter(user=request.user).first()
            dealer_address, created = DealerAddress.objects.get_or_create(
                dealer=dealer,
                address_line_1=address
            )
            dealer_address.dealer = dealer
            dealer_address.address_line_1 = address
            dealer_address.city = city
            dealer_address.state = state
            dealer_address.save()
        return JsonResponse({
            "status": "success",
            "message": "Profile updated successfully...",
        })
