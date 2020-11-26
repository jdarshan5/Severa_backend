from django.contrib import admin
from .models import UserMoment, MomentTags, MomentHashtags

# Register your models here.

admin.site.register(UserMoment)
admin.site.register(MomentTags)
admin.site.register(MomentHashtags)
