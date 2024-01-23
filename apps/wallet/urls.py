from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from apps.wallet.views import WalletView, FundWalletView

urlpatterns = [
    # path('validate_bvn/',  csrf_exempt(ValidateBVN.as_view()), name='validate_bvn'),
    path('<str:uid>/', WalletView.as_view(), name='get_wallet'),
    path('fund/<str:uid>/', csrf_exempt(FundWalletView.as_view()), name='fund_wallet'),
]
