from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['userProfileId']


admin.site.register(UserProfile, UserProfileAdmin)
