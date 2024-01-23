from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from apps.profiles import views


urlpatterns = [
    path('<slug:slug>/', views.ProfileView.as_view(), name='profile_detail'),
    path('<slug:slug>/get_profile_data/', views.GetProfileData.as_view(), name='get_profile_data'),
    path('<slug:slug>/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
]
