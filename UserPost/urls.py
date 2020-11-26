from django.urls import path

from . import views

urlpatterns = [
    path('registerPost/', views.register_post),
    path('updatePost/', views.update_post),
    path('deletePost/', views.delete_post),
    path('myPosts/', views.get_my_all_posts),
    path('requestPost/', views.get_post_of_user),
    path('likePost/', views.like_post),
    path('unlikePost/', views.unlike_post),
]
