from django.contrib import admin
from .models import UserPost, PostLike, PostTag, PostComment, PostHashtag

# Register your models here.

admin.site.register(UserPost)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(PostTag)
admin.site.register(PostHashtag)
