# Generated by Django 4.2.9 on 2024-01-30 23:54

import autoslug.fields
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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='user', unique=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Others', max_length=20, verbose_name='Gender')),
                ('bio', models.TextField(blank=True, default='Say something about yourself', null=True, verbose_name='About me')),
                ('image', cloudinary.models.CloudinaryField(blank=True, help_text='You profile image', max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='First&Last Name')),
                ('phone_number', phone_field.models.PhoneField(blank=True, default='', max_length=14, null=True)),
                ('birth_day', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, default='Nigeria', max_length=220, null=True, verbose_name='Country')),
                ('state', models.CharField(blank=True, max_length=220, null=True, verbose_name='State')),
                ('city', models.CharField(blank=True, max_length=220, null=True, verbose_name='City')),
                ('local_area', models.CharField(blank=True, default='', max_length=220, null=True, verbose_name='Area/Locale')),
                ('address', models.CharField(blank=True, default='', max_length=220, null=True, verbose_name='Address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
