import cloudinary
from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import requests
from phone_field import PhoneField
from apps.accounts.models import User


def upload_dir(instance, filename):
    return f"user_photos/{instance.user.username}/{filename}"


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Others", _("Others")


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='user', unique=True, always_update=True)
    gender = models.CharField(verbose_name=_("Gender"), max_length=20, choices=Gender.choices, default=Gender.OTHER)
    bio = models.TextField(verbose_name=_("About me"), default="Say something about yourself", blank=True, null=True)
    image = CloudinaryField(
        folder='UsersImages',
        blank=True,
        null=True,
        help_text="You profile image",
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    full_name = models.CharField(verbose_name=_("First&Last Name"), max_length=20, blank=True, null=True)
    phone_number = PhoneField(max_length=14, blank=True, null=True, default="")
    birth_day = models.DateField(blank=True, null=True)
    country = models.CharField(verbose_name=_("Country"), max_length=220, default="Nigeria", blank=True, null=True)
    state = models.CharField(verbose_name=_("State"), max_length=220, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=220, blank=True, null=True)
    local_area = models.CharField(verbose_name=_("Area/Locale"), max_length=220, default="", blank=True, null=True)
    address = models.CharField(verbose_name=_("Address"), max_length=220, default="", blank=True, null=True)
    # notifications = models.ManyToManyField(Notification, blank=True, null=True, related_name='notifications')

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse('profiles:profile_detail', kwargs={'slug': self.slug})

    def get_user_address(self):
        return f"{self.address} {self.city} {self.state} Nigeria"

    @property
    def image_url(self):
        if not self.image:
            if self.gender == "Female":
                return "https://img.icons8.com/fluency/48/null/person-female.png"
            elif self.gender == "Male":
                return "https://img.icons8.com/fluency/48/null/person-male.png"
            return "https://img.icons8.com/fluency/48/null/user-male-circle.png"
        return self.image.url

    @property
    def get_full_name(self):
        return f"{self.full_name.title()}" if self.full_name else f"{self.user.username.title()}"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    # Check if a profile already exists for this user
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
        print("Profile created!")

    # Update profile information if it's a social account
    if instance.socialaccount_set.exists():
        social_account = instance.socialaccount_set.first()

        if not instance.profile.image:
            # Update profile image, phone, country, state, address, etc.
            image_url = social_account.extra_data.get('picture', '')
            image_filename = f"profile_image_{instance.username}"
            # Download the image and save it to Cloudinary
            response = requests.get(image_url)
            if response.status_code == 200:
                # Upload the image to Cloudinary and set it as the profile image
                cloudinary.uploader.upload(response.content, public_id=image_filename)
                instance.profile.image = image_filename
                print("Profile image downloaded and saved!")

        instance.profile.full_name = social_account.extra_data.get('name', '')

        # Save the profile
        instance.profile.save()
        print("Profile updated!")
