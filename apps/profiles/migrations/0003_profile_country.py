# Generated by Django 4.2.7 on 2024-01-19 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_city_profile_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, default='Nigeria', max_length=220, null=True, verbose_name='Country'),
        ),
    ]
