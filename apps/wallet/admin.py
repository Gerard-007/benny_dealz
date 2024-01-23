from django.contrib import admin

from apps.wallet.models import Wallet, WalletTransactions

admin.site.register(Wallet)
admin.site.register(WalletTransactions)
