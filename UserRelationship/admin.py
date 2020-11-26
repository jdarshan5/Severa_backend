from django.contrib import admin
from .models import UserRelationship

# Register your models here.


class UserRelationshipAdmin(admin.ModelAdmin):
    readonly_fields = ['relationshipId', ]


admin.site.register(UserRelationship, UserRelationshipAdmin)
