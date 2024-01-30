import datetime
import random
import cloudinary
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from benny_dealz.utils import unique_slug_generator
from apps.cars.car_utils import MANUFACTURERS, STATUS, YEAR_CHOICES, CATEGORY, BODY_TYPE, TRANSMISSION, FUEL_TYPE, SWAP_STATUS
from apps.notifications.models import Notification
from django.db.models.signals import pre_save, pre_delete, post_save
from apps.accounts.models import User


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='user_favorites')


class CarQuerySet(models.query.QuerySet):
    def available_car(self):
        return self.filter(status="Available")


class CarManager(models.Manager):
    def get_queryset(self):
        return CarQuerySet(self.model, using=self._db)


class Car(models.Model):
    dealer = models.ForeignKey('dealers.Dealer', on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    brand_logo = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default="Available")
    car_inspection = models.BooleanField(default=False)
    can_be_swapped = models.BooleanField(help_text="Can this car be swapped with other cars from other users?", default=False)
    model_year = models.IntegerField('year', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    condition = models.CharField(max_length=100, choices=CATEGORY)
    body_type = models.CharField(max_length=100, choices=BODY_TYPE)
    main_image = CloudinaryField(
        folder='Dealer_Car_Main_Image',
        blank=True,
        null=True,
        help_text="Main image of the car",
        transformation={
            "quality": "auto:eco",
            "width": 500,  # Specify the desired width
            "height": 300,  # Specify the desired height
            "crop": "fill",  # Specify the crop mode (fill, fit, etc.)
        },
        resource_type="image",
    )
    mileage = models.IntegerField(blank=True, null=True, help_text='Enter valid mileage (1-1000000)')
    transmission = models.CharField(choices=TRANSMISSION, max_length=100)
    power = models.IntegerField(help_text="Car horse power measures in 'hp'...", blank=True, null=True)
    engine_size = models.IntegerField(help_text="cc", blank=True, null=True)
    number_of_cylinder = models.IntegerField(help_text="Number of cylinders", blank=True, null=True)
    number_of_seats = models.IntegerField(blank=True, null=True)
    fuel = models.CharField(max_length=100, choices=FUEL_TYPE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    description = models.TextField()
    address = models.ForeignKey("dealers.DealerAddress", on_delete=models.DO_NOTHING, null=True)

    date = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    favorited_by = models.ManyToManyField(User, through=Favorite, related_name='favorite_cars')

    # ============Car Feature===========
    coolBox = models.BooleanField(default=False)
    sunroof = models.BooleanField(default=False)
    DVDSystem = models.BooleanField(default=False)
    remoteKey = models.BooleanField(default=False)
    carTracker = models.BooleanField(default=False)
    parkAssist = models.BooleanField(default=False)
    heatedSeats = models.BooleanField(default=False)
    parkingSensor = models.BooleanField(default=False)
    pushStart = models.BooleanField(default=False)
    reverseCamera = models.BooleanField(default=False)
    navigationSystem = models.BooleanField(default=False)
    bluetoothHandsFree = models.BooleanField(default=False)
    audioSystem = models.BooleanField(default=False)

    objects = CarManager()

    class Meta:
        verbose_name_plural = "Cars"
        ordering = ("-date",)
        unique_together = ["brand", "model", "dealer"]

    def __str__(self):
        return f'{self.dealer.user}-{self.brand}'

    @property
    def get_car_name(self):
        return f'{self.brand}-{self.model}-{self.model_year}'

    @property
    def name(self):
        return f'Car-{self.brand}-{self.model}-{self.model_year}-{random.randint(0000, 9999)}'

    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'slug': self.slug})

    @property
    def get_main_image(self, *args, **kwargs):
        if self.main_image:
            return self.main_image.url
        return "https://res.cloudinary.com/bennydeals/image/upload/v1629781083/bgs/Bg_image_xc5kqn.jpg"


@receiver(pre_save, sender=Car)
def car_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_delete, sender=Car)
def car_images_delete(sender, instance, **kwargs):
    if instance.main_image:
        cloudinary.uploader.destroy(instance.main_image.public_id)


class CarMedia(models.Model):
    car = models.ForeignKey(Car, related_name="car_images", on_delete=models.CASCADE, blank=True, null=True)
    image = CloudinaryField(
        folder='Dealer_Car_Main_Image',
        blank=True,
        null=True,
        help_text="Main image of the car",
        transformation={
            "quality": "auto:eco",
            "width": 500,  # Specify the desired width
            "height": 300,  # Specify the desired height
            "crop": "fill",  # Specify the crop mode (fill, fit, etc.)
        },
        resource_type="image",
    )
    uploaded_by = models.ForeignKey(User, related_name="my_car_images", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.image.url}"


@receiver(pre_delete, sender=CarMedia)
def car_images_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


class CarSwap(models.Model):
    brand = models.CharField(max_length=100, choices=MANUFACTURERS)
    model = models.CharField(max_length=100)
    model_year = models.IntegerField('year', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    body_type = models.CharField(max_length=100, choices=BODY_TYPE)
    status = models.CharField(max_length=100, choices=SWAP_STATUS, default="Swap")
    condition = models.CharField(max_length=100, choices=CATEGORY, default="Nigerian Used")
    transmission = models.CharField(choices=TRANSMISSION, max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey("accounts.User", related_name='owner', on_delete=models.CASCADE)
    image = CloudinaryField(
        folder='Car_Swap_Image',
        blank=True,
        null=True,
        help_text="Main image of the car",
        transformation={
            "quality": "auto:eco",
            "width": 500,  # Specify the desired width
            "height": 300,  # Specify the desired height
            "crop": "fill",  # Specify the crop mode (fill, fit, etc.)
        },
        resource_type="image",
    )
    price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} for a swap..."

    class Meta:
        ordering = ('-date',)

    @property
    def get_car_swap_main_image(self, *args, **kwargs):
        if self.image:
            return self.image.url
        return "https://res.cloudinary.com/bennydeals/image/upload/v1629781083/bgs/Bg_image_xc5kqn.jpg"

    @property
    def get_car_swap_name(self):
        return f'Swap-{self.brand}-{self.model}-{self.model_year}'

    @property
    def name(self):
        return f'Swap-{self.brand}-{self.model}-{self.model_year}-{self.pk}'


@receiver(pre_save, sender=CarSwap)
def car_swap_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_delete, sender=CarSwap)
def car_swap_image_delete(sender, instance, **kwargs):
    if instance.main_image:
        cloudinary.uploader.destroy(instance.main_image.public_id)


class Comment(models.Model):
    car = models.ForeignKey(
        to="Car",
        on_delete=models.CASCADE,
        related_name='car_comment',
        blank=True,
        null=True
    )
    by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.content}-{self.by}'

    class Meta:
        ordering = ['-created_on']


@receiver(post_save, sender=Comment)
def user_add_comment_property(sender, instance, *args, **kwargs):
    comment = instance
    comm_car = comment.car
    sender = comment.by
    text_preview = comment.content[:50]
    message = f"{comment.by} just commented at {comm_car.brand}"
    notify = Notification(
        comment=comment,
        from_user=sender,
        to_user=comm_car.dealer.name,
        text_preview=text_preview,
        notification_type=2,
        message=message,
    )
    notify.save()
