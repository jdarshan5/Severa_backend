from django.urls import path

from UserRelationship import views

urlpatterns = [
    path('relationshipRequest/', views.request_relationship),
    path('followings/', views.get_my_following_relationships),
    path('followers/', views.get_my_follower_relationships),
    path('pendingRelationships/', views.pending_relationships),
    path('followingCount/', views.following_count),
    path('followerCount/', views.follower_count),
    path('blockRelation/', views.block_relation),
    path('declineRelation/', views.decline_relationship),
    path('acceptRelation/', views.accept_relationship),
    path('cancelRelation/', views.cancel_relationship),
]
