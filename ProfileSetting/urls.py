from django.urls import path

from ProfileSetting import views

urlpatterns = [
    path('getProfileSetting/', views.get_profile_setting),
    path('alterProtection/', views.alter_profile_protection),
]
