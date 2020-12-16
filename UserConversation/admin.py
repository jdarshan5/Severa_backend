from django.contrib import admin
from .models import UserConversation, UserMessages, SharedFile

# Register your models here.


class UserConversationAdmin(admin.ModelAdmin):
    readonly_fields = ['conversationId', ]


admin.site.register(UserConversation, UserConversationAdmin)


class UserMessagesAdmin(admin.ModelAdmin):
    readonly_fields = ['messageId', ]


admin.site.register(UserMessages, UserMessagesAdmin)
admin.site.register(SharedFile)
