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
    path('postComment/', views.post_comment),
    path('deleteComment/', views.delete_post_comment),
    path('postSubComment/', views.post_sub_comment),
    path('deleteSubComment/', views.delete_post_sub_comment),
    path('addUserTagInPost/', views.add_user_tag_in_post),
]
