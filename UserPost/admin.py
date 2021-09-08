from django.contrib import admin
from .models import UserPost, PostLike, PostTag, PostComment, PostHashtag, PostSubComment

# Register your models here.


class UserPostAdmin(admin.ModelAdmin):
    readonly_fields = ['postId', 'postTime', ]


admin.site.register(UserPost, UserPostAdmin)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(PostTag)
admin.site.register(PostHashtag)
admin.site.register(PostSubComment)
