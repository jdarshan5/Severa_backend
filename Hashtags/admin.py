from django.contrib import admin
from .models import Hashtag

# Register your models here.


class HashtagAdmin(admin.ModelAdmin):
    readonly_fields = ['hashtagId']
    ordering = ['hashtagName']


admin.site.register(Hashtag, HashtagAdmin)
