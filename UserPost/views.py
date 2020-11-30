from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from UserProfiles.models import UserProfile

from rest_framework.response import Response

from .serializers import RegisterPostSerializer, UserPostSerializer, PostLikeSerializer, PostCommentSerializer,\
    PostSubCommentSerializer, PostTagSerializer
from .models import UserPost, PostLike, PostComment, PostSubComment, PostTag

from ProfileSetting.models import UserSetting

from UserRelationship.models import UserRelationship

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_post(request):
    data = {}
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    file = request.FILES['postContent']
    data['userProfileId'] = user_profile.id
    data['postContent'] = file
    data['postDescription'] = request.data['postDescription']
    serializer = RegisterPostSerializer(data=data)
    if serializer.is_valid():
        post = serializer.save()
        post_serializer = UserPostSerializer(post)
        return Response(post_serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request):
    data = {}
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post = UserPost.objects.get(postId=request.data['postId'])
    if post.userProfileId == user_profile:
        data['postDescription'] = request.data['postDescription']
        post_serializer = UserPostSerializer(post, data=data, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data)
        else:
            return Response(post_serializer.errors)
    else:
        return Response({"You're not the owner of the post"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post = UserPost.objects.get(postId=request.data['postId'])
    if user_profile == post.userProfileId:
        post.delete()
        return Response({'POST deleted'})
    return Response({"You're not the owner of the post"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_all_posts(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post_list = UserPost.objects.filter(userProfileId=user_profile)
    if post_list:
        serializer = UserPostSerializer(post_list, many=True)
        return Response(serializer.data)
    return Response({})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_of_user(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    requested_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    requested_profile_setting = UserSetting.objects.get(userProfile=requested_profile)
    requested_relation = UserRelationship.objects.filter(followingId=requested_profile).filter(followerId=user_profile)
    if requested_profile_setting.protected == 1:
        # Private Account
        if not requested_relation:
            # relation does not exist
            relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)
            if not relation:
                return Response({})
            else:
                if relation[0].relationshipStatus == 1:
                    post_list = UserPost.objects.filter(userProfileId=requested_profile)
                    serializer = UserPostSerializer(post_list, many=True)
                    return Response(serializer.data)
                else:
                    return Response({})
        else:
            if requested_relation[0].relationshipStatus != 3:
                relation = \
                    UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)
                if not relation:
                    return Response({})
                else:
                    if relation[0].relationshipStatus == 1:
                        post_list = UserPost.objects.filter(userProfileId=requested_profile)
                        serializer = UserPostSerializer(post_list, many=True)
                        return Response(serializer.data)
                    else:
                        return Response({})
    else:
        # Public Account
        if not requested_relation:
            relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)
            if not relation:
                post_list = UserPost.objects.filter(userProfieId=requested_profile)
                serializer = UserPostSerializer(post_list, many=True)
                return Response(serializer.data)
            else:
                if relation[0].relationshipStatus == 3:
                    return Response({})
                post_list = UserPost.objects.filter(userProfieId=requested_profile)
                serializer = UserPostSerializer(post_list, many=True)
                return Response(serializer.data)
        else:
            if requested_relation[0].relationshipStatus == 3:
                return Response({})
            relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)
            if not relation:
                post_list = UserPost.objects.filter(userProfileId=requested_profile)
                serializer = UserPostSerializer(post_list, many=True)
                return Response(serializer.data)
            else:
                if relation[0].relationshipStatus == 3:
                    return Response({})
                post_list = UserPost.objects.filter(userProfileId=requested_profile)
                serializer = UserPostSerializer(post_list, many=True)
                return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request):
    data = {}
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post = UserPost.objects.get(postId=request.POST['postId'])
    data['userProfileId'] = user_profile.id
    data['postId'] = post.id
    serializer = PostLikeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_post(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post = UserPost.objects.get(postId=request.data['postId'])
    post_like = PostLike.objects.filter(postId=post).filter(userProfileId=user_profile)
    post_like[0].delete()
    post_like[0].save()
    return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_comment(request):
    data = {}
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post = UserPost.objects.get(postId=request.data['postId'])
    data['userProfileId'] = user_profile
    data['postId'] = post
    data['commentDescription'] = request.data['commentDescription']
    serializer = PostCommentSerializer(data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post_comment(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    comment = PostComment.objects.filter(userProfileId=user_profile).filter(postId=request.data['postId'])\
        .filter(commentId=request.data['commentId'])
    comment[0].delete()
    comment[0].save()
    return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_sub_comment(request):
    data = {}
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    data['userProfileId'] = user_profile
    data['commentId'] = request.data['commentId']
    data['commentDescription'] = request.data['commentDescription']
    serializer = PostSubCommentSerializer(data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post_sub_comment(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    comment = PostSubComment.objects.filter(userProfileId=user_profile).filter(postId=request.data['postId']) \
        .filter(commentId=request.data['subCommentId'])
    comment[0].delete()
    comment[0].save()
    return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_tag_in_post(request):
    data = {'userProfileId': UserProfile.objects.get(userId=request.data['taggedUser']),
            'postId': request.data['postId']}
    serializer = PostTagSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)
