# Generated by Django 4.2.9 on 2024-02-03 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0001_initial'),
        ('wallet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField(choices=[(1, 'Dealer_Message'), (2, 'Comment_Message'), (3, 'Transaction_Message'), (4, 'User_Message'), (5, 'Car_Message')])),
                ('from_admin', models.CharField(blank=True, default='System Notification', max_length=100, null=True)),
                ('text_preview', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car_notifications', to='cars.car')),
                ('car_swap', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car_swap_notifications', to='cars.carswap')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_notifications', to='cars.comment')),
                ('from_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_from', to=settings.AUTH_USER_MODEL)),
                ('message_dealer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dealer_message', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_to', to=settings.AUTH_USER_MODEL)),
                ('wallet_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallet_transaction_notifications', to='wallet.wallettransactions')),
            ],
        ),
    ]
