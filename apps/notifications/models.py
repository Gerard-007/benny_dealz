from django.conf import settings
from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Dealer_Message'),
        (2, 'Comment_Message'),
        (3, 'Transaction_Message'),
        (4, 'User_Message'),
        (5, 'Car_Message'),
    )
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_to', on_delete=models.CASCADE, blank=True, null=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_from', on_delete=models.CASCADE, blank=True, null=True)
    from_admin = models.CharField(max_length=100, blank=True, null=True, default="System Notification")
    message_dealer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dealer_message', on_delete=models.CASCADE, blank=True, null=True)
    # user_message = models.ForeignKey('accounts.UserMessage', related_name='user_message', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey('cars.Comment', related_name='comment_notifications', on_delete=models.CASCADE, blank=True, null=True)
    car_swap = models.ForeignKey('cars.CarSwap', related_name='car_swap_notifications', on_delete=models.CASCADE, blank=True, null=True)
    car = models.ForeignKey('cars.Car', related_name='car_notifications', on_delete=models.CASCADE, blank=True, null=True)
    wallet_transaction = models.ForeignKey('wallet.WalletTransactions', related_name='wallet_transaction_notifications', on_delete=models.CASCADE, blank=True, null=True)
    text_preview = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user}-{self.to_user}"
