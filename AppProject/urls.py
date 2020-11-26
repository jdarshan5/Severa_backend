from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Account.urls')),
    path('', include('UserProfiles.urls')),
    path('', include('UserRelationship.urls')),
    path('', include('UserPost.urls')),
    path('', include('ProfileSetting.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
