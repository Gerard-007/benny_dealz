from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from apps.cars import views
from apps.cars.views import ToggleFavoriteView

urlpatterns = [
    # path('dashboard/', views.CarDashBoard.as_view(), name='car_dashboard'),
    path('featuring/<slug:slug>/', views.CarFeatureUpgrade.as_view(), name='car_featuring'),
    path('swap_list/', views.CarSwapListView.as_view(), name='swap_list'),
    path('swap_create/', views.CarSwapCreateView.as_view(), name='swap_create'),
    path('swap_delete/<slug:slug>', views.CarSwapDeleteView.as_view(), name='swap_delete'),
    path('toggle_favorite/<int:car_id>/', csrf_exempt(ToggleFavoriteView.as_view()), name='toggle_favorite'),
    path('remove_favorite/<int:car_id>/', csrf_exempt(views.RemoveFavoriteView.as_view()), name='remove_favorite'),
    path('list_favorite/', csrf_exempt(views.FavouriteCars.as_view()), name='list_favorite'),
    path('create/', views.CarCreateView.as_view(), name='create'),
    path('edit/', views.CarUpdateView.as_view(), name='update'),
    path('delete/', views.CarDeleteView.as_view(), name='delete'),
    path('<slug:slug>/', views.CarDetailView.as_view(), name='detail'),
    path('', views.CarListView.as_view(), name='list'),
]
