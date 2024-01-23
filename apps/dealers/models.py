import cloudinary
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from urllib.parse import urlencode
import requests
from phone_field import PhoneField

from apps.accounts.models import User
from benny_dealz.utils import unique_slug_generator


class DealerQuerySet(models.query.QuerySet):
    def an_active_dealer(self):
        return self.filter(dealer_active=True)


class DealerManager(models.Manager):
    def get_queryset(self):
        return DealerQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().an_active_dealer()


class Dealer(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="user_dealer")
    business_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    # slug = AutoSlugField(populate_from='business_name', unique=True, always_update=True)
    business_email = models.EmailField(max_length=100, blank=True, null=True)
    business_phone = PhoneField(blank=True, null=True)
    business_logo = CloudinaryField(
        folder='User_Dealer_Business_logos',
        blank=True,
        null=True,
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    t_and_a = models.BooleanField(default=True)
    dealer_active = models.BooleanField(default=True)
    objects = DealerManager()

    def __str__(self):
        return f"{self.user.username}-{self.business_name}"

    def get_absolute_url(self):
        return reverse('dealers:detail', kwargs={'slug': self.slug})

    def total_view_counts(self):
        # Calculate the sum of view counts for all cars associated with the dealer
        return self.cars.aggregate(Sum('view_count'))['view_count__sum'] or 0

    def get_business_logo(self):
        return (
            self.business_logo.url
            if self.business_logo
            else "https://res.cloudinary.com/bennydeals/image/upload/v1629781082/bgs/bennydealz_bg3_otuymc.png"
        )

    @property
    def name(self):
        return self.business_name

    @property
    def dealer_email(self):
        return self.business_email or self.name.email

    def save(self, *args, **kwargs):
        get_current_user = User.objects.get(email=self.user.email)
        try:
            get_current_user.is_a_dealer = True
            get_current_user.save()
        except ModuleNotFoundError:
            get_current_user.is_a_dealer = False
            get_current_user.save()
            get_current_user.refresh_from_db()
        super(Dealer, self).save(*args, **kwargs)


@receiver(pre_save, sender=Dealer)
def dealer_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# === Deactivate user as Dealer & ===
@receiver(pre_delete, sender=Dealer)
def dealer_pre_delete_receiver(sender, instance, *args, **kwargs):
    current_user_dealer = User.objects.get(username=instance.user.username)
    print(current_user_dealer.username)
    current_user_dealer.is_a_dealer = False
    current_user_dealer.save()


@receiver(pre_delete, sender=Dealer)
def dealer_avatar_delete(sender, instance, **kwargs):
    if instance.business_logo:
        cloudinary.uploader.destroy(instance.business_logo.public_id)


class DealerAddress(models.Model):
    dealer = models.ForeignKey(to="Dealer", on_delete=models.CASCADE, related_name='addresses')
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Nigeria')
    postal_code = models.CharField(max_length=120, default='234')
    longitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)

    @property
    def get_dealer_address(self):
        if len(self.address_line_1) > 10:
            self.address_line_1 = f"{self.address_line_1[:10]}..."
            return f"{self.address_line_1}, {self.address_line_2}, {self.city}, {self.state}"
        return f"{self.address_line_1}, {self.address_line_2}, {self.city}, {self.state}"


# Update <is_a_dealer> to <False> once instance is deleted
@receiver(pre_delete, sender=Dealer)
def user_dealership_status_update(sender, instance, *args, **kwargs):
    dealer = instance
    # Update dealer status
    user = User.objects.get(username=dealer.user.username)
    user.is_a_dealer = False
    user.save(update_fields=['is_a_dealer'])


def address_pre_save(sender, instance, *args, **kwargs):
    try:
        here_api = "BsI7Qnbq78Ca-bgKr64h49euv3Zo7WuYChK3bJI-ce0"
        address = f"{str(instance.address_line_1)} {str(instance.address_line_2)} {str(instance.city)} {str(instance.state)} {str(instance.postal_code)} {str(instance.country)}"
        params = {'apiKey': here_api, 'searchtext': address}
        endpoint = "https://geocoder.ls.hereapi.com/6.2/geocode.json?"
        url_param = urlencode(params)
        url = f"{endpoint}{url_param}"
        r = requests.get(url)
        instance.longitude = r.json()['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']
        instance.latitude = r.json()['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
    except Exception:
        print(Exception)


pre_save.connect(address_pre_save, sender=Dealer)
