from django.urls import path
from UserProfiles import views

urlpatterns = [
    path('profileById/', views.get_small_profile_by_id),
    path('allProfiles/', views.get_all_profiles),
    path('searchProfile/', views.search_profiles),
    path('fullProfileById/', views.get_full_profile_by_id),
    path('changeProfilePicture/', views.change_profile_picture),
    path('changeProfileDescription/', views.change_profile_description),
    path('getSelfProfileId/', views.get_profile_id),
]
