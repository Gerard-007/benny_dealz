# Generated by Django 4.2.9 on 2024-02-05 08:49

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dealers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('brand_logo', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('status', models.CharField(choices=[('Sold', 'Sold'), ('Available', 'Available'), ('Rented', 'Rented'), ('Swapped', 'Swapped')], default='Available', max_length=100)),
                ('car_inspection', models.BooleanField(default=False)),
                ('can_be_swapped', models.BooleanField(default=False, help_text='Can this car be swapped with other cars from other users?')),
                ('model_year', models.IntegerField(choices=[(1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], default=2024, verbose_name='year')),
                ('condition', models.CharField(choices=[('New', 'New'), ('Foreign Used', 'Foreign Used'), ('Nigerian Used', 'Nigerian Used')], max_length=100)),
                ('body_type', models.CharField(choices=[('Bus', 'Bus'), ('Coupe', 'Coupe'), ('Hatchback', 'Hatchback'), ('Pickup', 'Pickup'), ('Suv', 'Suv'), ('Convertible', 'Convertible'), ('Crossover', 'Crossover'), ('Mpv', 'Mpv'), ('Sedan', 'Sedan'), ('Truck', 'Truck'), ('Electric', 'Electric'), ('Luxury', 'Luxury'), ('Wagon', 'Wagon'), ('Compact', 'Compact'), ('Sports', 'Sports')], max_length=100)),
                ('main_image', cloudinary.models.CloudinaryField(blank=True, help_text='Main image of the car', max_length=255, null=True)),
                ('mileage', models.IntegerField(blank=True, help_text='Enter valid mileage (1-1000000)', null=True)),
                ('transmission', models.CharField(choices=[('Manual', 'Manual'), ('Automatic', 'Automatic'), ('Duplex', 'Duplex')], max_length=100)),
                ('power', models.IntegerField(blank=True, help_text="Car horse power measures in 'hp'...", null=True)),
                ('engine_size', models.IntegerField(blank=True, help_text='cc', null=True)),
                ('number_of_cylinder', models.IntegerField(blank=True, help_text='Number of cylinders', null=True)),
                ('number_of_seats', models.IntegerField(blank=True, null=True)),
                ('fuel', models.CharField(choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('CNG', 'CNG'), ('Hybrid', 'Hybrid'), ('Electric', 'Electric')], max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=19)),
                ('description', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('view_count', models.IntegerField(default=0)),
                ('coolBox', models.BooleanField(default=False)),
                ('sunroof', models.BooleanField(default=False)),
                ('DVDSystem', models.BooleanField(default=False)),
                ('remoteKey', models.BooleanField(default=False)),
                ('carTracker', models.BooleanField(default=False)),
                ('parkAssist', models.BooleanField(default=False)),
                ('heatedSeats', models.BooleanField(default=False)),
                ('parkingSensor', models.BooleanField(default=False)),
                ('pushStart', models.BooleanField(default=False)),
                ('reverseCamera', models.BooleanField(default=False)),
                ('navigationSystem', models.BooleanField(default=False)),
                ('bluetoothHandsFree', models.BooleanField(default=False)),
                ('audioSystem', models.BooleanField(default=False)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dealers.dealeraddress')),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='dealers.dealer')),
            ],
            options={
                'verbose_name_plural': 'Cars',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorites', to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car_comment', to='cars.car')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='CarSwap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(choices=[('Abarth', 'Abarth'), ('Alfa Romeo', 'Alfa Romeo'), ('Aston Martin', 'Aston Martin'), ('Audi', 'Audi'), ('Bentley', 'Bentley'), ('BMW', 'BMW'), ('Bugatti', 'Bugatti'), ('Cadillac', 'Cadillac'), ('Chevrolet', 'Chevrolet'), ('Chrysler', 'Chrysler'), ('Citroën', 'Citroën'), ('Dacia', 'Dacia'), ('Daewoo', 'Daewoo'), ('Daihatsu', 'Daihatsu'), ('Dodge', 'Dodge'), ('Donkervoort', 'Donkervoort'), ('DS', 'DS'), ('Ferrari', 'Ferrari'), ('Fiat', 'Fiat'), ('Fisker', 'Fisker'), ('Ford', 'Ford'), ('Honda', 'Honda'), ('Hummer', 'Hummer'), ('Hyundai', 'Hyundai'), ('Infiniti', 'Infiniti'), ('Innoson', 'Innoson'), ('Iveco', 'Iveco'), ('Jaguar', 'Jaguar'), ('Jeep', 'Jeep'), ('Kia', 'Kia'), ('KTM', 'KTM'), ('Lada', 'Lada'), ('Lamborghini', 'Lamborghini'), ('Lancia', 'Lancia'), ('Land Rover', 'Land Rover'), ('Landwind', 'Landwind'), ('Lexus', 'Lexus'), ('Lotus', 'Lotus'), ('Maserati', 'Maserati'), ('Maybach', 'Maybach'), ('Mazda', 'Mazda'), ('McLaren', 'McLaren'), ('Mercedes-Benz', 'Mercedes-Benz'), ('MG', 'MG'), ('Mini', 'Mini'), ('Mitsubishi', 'Mitsubishi'), ('Morgan', 'Morgan'), ('Nissan', 'Nissan'), ('Opel', 'Opel'), ('Peugeot', 'Peugeot'), ('Porsche', 'Porsche'), ('Renault', 'Renault'), ('Rolls-Royce', 'Rolls-Royce'), ('Rover', 'Rover'), ('Saab', 'Saab'), ('Seat', 'Seat'), ('Skoda', 'Skoda'), ('Smart', 'Smart'), ('SsangYong', 'SsangYong'), ('Subaru', 'Subaru'), ('Suzuki', 'Suzuki'), ('Tesla', 'Tesla'), ('Toyota', 'Toyota'), ('Volkswagen', 'Volkswagen'), ('Volvo', 'Volvo')], max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('model_year', models.IntegerField(choices=[(1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], default=2024, verbose_name='year')),
                ('body_type', models.CharField(choices=[('Bus', 'Bus'), ('Coupe', 'Coupe'), ('Hatchback', 'Hatchback'), ('Pickup', 'Pickup'), ('Suv', 'Suv'), ('Convertible', 'Convertible'), ('Crossover', 'Crossover'), ('Mpv', 'Mpv'), ('Sedan', 'Sedan'), ('Truck', 'Truck'), ('Electric', 'Electric'), ('Luxury', 'Luxury'), ('Wagon', 'Wagon'), ('Compact', 'Compact'), ('Sports', 'Sports')], max_length=100)),
                ('status', models.CharField(choices=[('Swap', 'Swap'), ('Sell', 'Sell')], default='Swap', max_length=100)),
                ('condition', models.CharField(choices=[('New', 'New'), ('Foreign Used', 'Foreign Used'), ('Nigerian Used', 'Nigerian Used')], default='Nigerian Used', max_length=100)),
                ('transmission', models.CharField(choices=[('Manual', 'Manual'), ('Automatic', 'Automatic'), ('Duplex', 'Duplex')], max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('image', cloudinary.models.CloudinaryField(blank=True, help_text='Main image of the car', max_length=255, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='CarMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, help_text='Main image of the car', max_length=255, null=True)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car_images', to='cars.car')),
                ('uploaded_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_car_images', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='favorited_by',
            field=models.ManyToManyField(related_name='favorite_cars', through='cars.Favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='car',
            unique_together={('brand', 'model', 'dealer')},
        ),
    ]
