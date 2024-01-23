from django.contrib import admin
from apps.profiles.models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'slug',
        'gender',
    ]
    list_filter = ['gender']
    list_display_links = ['id', 'slug']
    readonly_fields = (
        'user',
    )


admin.site.register(Profile, ProfileAdmin)
