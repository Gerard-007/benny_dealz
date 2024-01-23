from django.urls import path
from apps.accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('set-new-password/<uidb64>/<token>/', views.CompletePasswordResetView.as_view(), name='reset-user-password'),
    path('reset/', views.PasswordResetView.as_view(), name='reset-password'),
    path('activate_account/', views.ActivateAccountView.as_view(), name='activate_account'),
]