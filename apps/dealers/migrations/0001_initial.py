# Generated by Django 4.2.9 on 2024-01-31 00:10

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('business_email', models.EmailField(blank=True, max_length=100, null=True)),
                ('business_phone', phone_field.models.PhoneField(blank=True, max_length=31, null=True)),
                ('business_logo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True)),
                ('t_and_a', models.BooleanField(default=True)),
                ('dealer_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dealer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DealerAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(max_length=120)),
                ('address_line_2', models.CharField(blank=True, max_length=120, null=True)),
                ('city', models.CharField(max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('country', models.CharField(default='Nigeria', max_length=120)),
                ('postal_code', models.CharField(default='234', max_length=120)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='dealers.dealer')),
            ],
        ),
    ]
