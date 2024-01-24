# Generated by Django 4.2.9 on 2024-01-24 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('currency', models.CharField(blank=True, choices=[('₦', 'NGN'), ('$', 'USD'), ('€', 'EUR'), ('£', 'GBP')], default='NGN', max_length=100, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=100, verbose_name='balance')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100, verbose_name='transaction')),
                ('currency', models.CharField(blank=True, choices=[('₦', 'NGN'), ('$', 'USD'), ('€', 'EUR'), ('£', 'GBP')], default='NGN', max_length=100, null=True, verbose_name='currency')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100, verbose_name='amount')),
                ('payment_status', models.CharField(choices=[('successful', 'successful'), ('pending', 'pending'), ('failed', 'failed')], max_length=100, verbose_name='payment status')),
                ('payment_gateway', models.CharField(default='flutterwave', max_length=100, verbose_name='payment gateway')),
                ('is_in_flow', models.BooleanField(default=False, verbose_name='concurrences')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wallet.wallet')),
            ],
        ),
    ]
