from django.urls import path
from apps.dealers.views import DealerCreateView, DealerDetailView, DealerUpdateView, DealerListView, \
    DealerDashboardView, DealerCarListView, DealerAddressCreateView, DealerAddressListView, DealerAddressUpdateView, \
    DealerAddressDeleteView


urlpatterns = [
    path('dealer_address_delete/', DealerAddressDeleteView.as_view(), name='dealer_address_delete'),
    path('dealer_address_update/', DealerAddressUpdateView.as_view(), name='dealer_address_update'),
    path('dealer_address_add/', DealerAddressCreateView.as_view(), name='dealer_address_add'),
    path('dealer_address_list/', DealerAddressListView.as_view(), name='dealer_address_list'),
    path('update/', DealerUpdateView.as_view(), name='dealer_update'),
    path('signup/', DealerCreateView.as_view(), name='dealer_signup'),
    path('dashboard/', DealerDashboardView.as_view(), name='dealer_dashboard'),
    path('dealer_car_list/', DealerCarListView.as_view(), name='dealer_car_list'),
    path('<slug:slug>/', DealerDetailView.as_view(), name='dealer_detail'),
    path('', DealerListView.as_view(), name='dealer_list'),
]
