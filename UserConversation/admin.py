from django.contrib import admin
from .models import UserConversation, UserMessages

# Register your models here.

admin.site.register(UserConversation)
admin.site.register(UserMessages)
