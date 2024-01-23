import uuid
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.dealers.models import Dealer
from apps.notifications.models import Notification

CURRENCY = (
    ("₦", "NGN"),
    ("$", "USD"),
    ("€", "EUR"),
    ("£", "GBP"),
)

STATUS = (
    ("successful", "successful"),
    ("pending", "pending"),
    ("failed", "failed"),
)


class Wallet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="wallet")
    currency = models.CharField(max_length=100, choices=CURRENCY, default="NGN", blank=True, null=True)
    balance = models.DecimalField(_("balance"), max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID {self.uid} -> {self.user.profile.get_full_name}"


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if instance.is_a_dealer:
        Wallet.objects.create(user=instance)
        print("Wallet created!")

    # if not hasattr(instance, 'wallet'):
    #     Wallet.objects.create(user=instance)
    #     print("Profile created!")


@receiver(post_delete, sender=User)
def delete_related_wallet(sender, instance, **kwargs):
    # Using filter instead of get to avoid DoesNotExist exception
    wallets = Wallet.objects.filter(user=instance)
    wallets.delete()


class WalletTransactions(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField(_("transaction"), max_length=100)
    currency = models.CharField(_("currency"), max_length=100, choices=CURRENCY, default="NGN", blank=True, null=True)
    amount = models.DecimalField(_("amount"), max_digits=100, decimal_places=2)
    payment_status = models.CharField(_("payment status"), max_length=100, choices=STATUS)
    payment_gateway = models.CharField(_("payment gateway"), max_length=100, default="flutterwave")
    is_in_flow = models.BooleanField(_("concurrences"), default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transactions for {self.wallet} id: {self.transaction_id}"


@receiver(post_delete, sender=Wallet)
def delete_related_wallet_transaction(sender, instance, **kwargs):
    # Using filter instead of get to avoid DoesNotExist exception
    wallet_trans = WalletTransactions.objects.filter(wallet=instance)
    wallet_trans.delete()


@receiver(post_save, sender=WalletTransactions)
def user_add_comment_property(sender, instance, *args, **kwargs):
    transaction = instance
    comm_car = transaction.wallet
    sender = "System Transaction Notifier"
    message = f"Transaction for {transaction.transaction_id} with amount {transaction.currency}{transaction.amount} was initiated.<br> Time-stamp: {transaction.timestamp}.<br> Transaction status: {transaction.payment_status}"
    notify = Notification(
        wallet_transaction=transaction,
        from_admin=sender,
        to_user=transaction.wallet.dealer.name,
        notification_type=3,
        message=message,
    )
    notify.save()
