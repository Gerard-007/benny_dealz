from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from benny_dealz.views import HomeView, AboutUs, ContactUs, GetStates, GetCities, GetCarBrands, GetCarModels, \
    check_phone, check_username, check_email, check_password, confirm_password, check_business_phone, \
    check_business_name, check_business_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('about/', AboutUs.as_view(), name="about"),
    path('contact/', ContactUs.as_view(), name="contact"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('social_accounts/', include('allauth.urls')),

    path('accounts/', include(('apps.accounts.urls', 'apps.accounts'), namespace='accounts')),
    path('api/accounts/', include(('apps.accounts.api.urls', 'apps.accounts'), namespace='api_accounts')),

    path('profiles/', include(('apps.profiles.urls', 'apps.profiles'), namespace='profiles')),
    path('api/profiles/', include(('apps.profiles.api.urls', 'apps.profiles'), namespace='profiles_api')),

    path('dealers/', include(('apps.dealers.urls', 'apps.dealers'), namespace='dealers')),
    # path('api/dealers/', include(('apps.dealers.api.urls', 'apps.dealers'), namespace='dealers_api')),

    path('cars/', include(('apps.cars.urls', 'apps.cars'), namespace='cars')),
    # path('api/cars/', include(('apps.cars.api.urls', 'apps.cars'), namespace='cars_api')),

    path('notifications/', include(('apps.notifications.urls', 'apps.notifications'), namespace='notifications')),
    # path('api/notifications/', include(('apps.notifications.api.urls', 'apps.notifications'), namespace='notifications_api')),

    path('wallet/', include(('apps.wallet.urls', 'apps.wallet'), namespace='wallet')),
    # path('api/wallet/', include(('apps.wallet.api.urls', 'apps.wallet'), namespace='wallet_api')),

    path('get_states/', csrf_exempt(GetStates.as_view()), name="get_states"),
    path('get_cities/', csrf_exempt(GetCities.as_view()), name="get_cities"),

    path('get_car_brands/', csrf_exempt(GetCarBrands.as_view()), name="get_car_brands"),
    path('get_car_brand_models/', csrf_exempt(GetCarModels.as_view()), name="get_car_brand_models"),

    # path('filtered_results/', FilterResultView.as_view(), name='filtered_results'),
    # path('chats/', include(('chats.urls', 'chats'), namespace='chats')),
    # path('conversations/', include(('conversations.urls', 'conversations'), namespace='conversations')),
]

htmx_urlpatterns = [
    path('check_username/', check_username, name="check_username"),
    path('check_email/', check_email, name="check_email"),
    path('check_password/', check_password, name="check_password"),
    path('confirm_password/', confirm_password, name="confirm_password"),
    path('check_phone/', check_phone, name='check_phone'),
    path('check_business_name/', check_business_name, name='check_business_name'),
    path('check_business_email/', check_business_email, name='check_business_email'),
    path('check_business_phone/', check_business_phone, name='check_business_phone'),
]

urlpatterns += htmx_urlpatterns


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path("500/", TemplateView.as_view(template_name='pages/500.html'), name="500"),
    path("403/", TemplateView.as_view(template_name='pages/403.html'), name="403"),
    re_path(r'^.*', TemplateView.as_view(template_name='pages/404.html'), name="404"),
]


admin.site.site_header = "Benny Dealz Admin"
admin.site.site_title = "Benny Dealz Admin Portal"
admin.site.site_title = "Welcome to the Benny Dealz administration"
