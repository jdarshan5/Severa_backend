from rest_framework import serializers
from .models import UserPost, PostLike, PostComment, PostTag, PostHashtag, PostSubComment


class RegisterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['userProfileId', 'postContent', 'postDescription']


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['userProfileId', 'postId', 'postContent', 'postDescription', 'postTime', 'postStatus']


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['userProfileId', 'postId', 'likeTime']


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['userProfileId', 'postId', 'commentId', 'commentDescription', 'commentTime', 'commentStatus']


class PostSubCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSubComment
        fields = ['userProfileId', 'parentComment', 'subCommentId', 'commentDescription', 'commentTime',
                  'commentStatus']


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ['taggedUserId', 'postId', 'postTagId']


class PostHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHashtag
        fields = ['postId', 'hashtagId']
