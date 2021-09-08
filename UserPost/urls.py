from django.urls import path

from . import views

urlpatterns = [
    path('registerPost/', views.register_post),
    path('updatePost/', views.update_post),
    path('deletePost/', views.delete_post),
    path('myPosts/', views.get_my_all_posts),
    path('requestPost/', views.get_post_of_user),
    path('likePost/', views.like_post),
    path('postLikeCount/', views.get_post_like_count),
    path('unlikePost/', views.unlike_post),
    path('postComment/', views.post_comment),
    path('postCommentCount/', views.get_post_comment_count),
    path('deleteComment/', views.delete_post_comment),
    path('postSubComment/', views.post_sub_comment),
    path('deleteSubComment/', views.delete_post_sub_comment),
    # path('addUserTagInPost/', views.add_user_tag_in_post),
    path('postDetail/', views.get_a_post_detail),
    path('getFeeds/', views.get_feeds),
    path('postLikes/', views.get_all_likes_on_a_post),
    path('postComments/', views.get_all_comments_on_a_post),
    path('noOfPosts/', views.get_no_of_posts),
]
