from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from UserProfiles.models import UserProfile
from UserProfiles.serializers import SmallDataUserProfileSerializer

from rest_framework.response import Response

from Account.models import Account

from .serializers import RegisterPostSerializer, UserPostSerializer, PostLikeSerializer, PostCommentSerializer,\
    PostSubCommentSerializer, PostTagSerializer, PostHashtagSerializer
from .models import UserPost, PostLike, PostComment, PostSubComment, PostTag, PostHashtag

from ProfileSetting.models import UserSetting

from UserRelationship.models import UserRelationship

from Hashtags.models import Hashtag
from Hashtags.serializers import HashtagSerializer

from Account.serializers import SmallDataAccountSerializer

import pandas as pd

# Create your views here.


def get_hashtags(post_description):
    pd_list = post_description.split()
    all_hashtags = []
    for value in pd_list:
        if value[0] == '#':
            all_hashtags.append(value[1:])
    return all_hashtags


def create_hashtag_instance(hashtags):
    for hashtag in hashtags:
        try:
            hashtag = Hashtag.objects.get(hashtagName=hashtag)
            continue
        except Hashtag.DoesNotExist:
            data = {'hashtagName': hashtag}
            serializer = HashtagSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)


def create_post_hashtag_instance(hashtags, post_id):
    for hashtag in hashtags:
        try:
            ht = Hashtag.objects.get(hashtagName=hashtag)
        except Hashtag.DoesNotExist:
            continue
        data = {'postId': post_id, 'hashtagId': ht.hashtagId}
        serializer = PostHashtagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            continue
        else:
            return Response(serializer.errors)


def get_tagged_ids(post_description):
    i = 0
    user_lst = {}
    while True:
        value = post_description.find('@', i)
        if value == -1:
            break
        i = value + 1
        if post_description[i] == ' ':
            continue
        user_lst.update({post_description[i:].split()[0]: i})
    return user_lst


def create_post_tag_instance(tagged_id_list, post_id):
    for user in tagged_id_list.keys():
        start_index = tagged_id_list[user]
        try:
            user_profile = UserProfile.objects.get(userId=Account.objects.get(userid=user))
        except (UserProfile.DoesNotExist, Account.DoesNotExist):
            continue
        data = {'taggedUserId': user_profile.id, 'postId': post_id, 'index': start_index}
        serializer = PostTagSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)


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
    hashtags = get_hashtags(data['postDescription'])
    create_hashtag_instance(hashtags)
    tagged_id_list = get_tagged_ids(data['postDescription'])
    serializer = RegisterPostSerializer(data=data)
    if serializer.is_valid():
        post = serializer.save()
        post_serializer = UserPostSerializer(post)
        create_post_hashtag_instance(hashtags, post.id)
        create_post_tag_instance(tagged_id_list, post.id)
        return Response(post_serializer.data)
    else:
        return Response(serializer.errors)


def get_new_hashtag_instances(hashtags):
    hashtag_list = []
    for hashtag in hashtags:
        try:
            h = Hashtag.objects.get(hashtagName=hashtag)
        except Hashtag.DoesNotExist:
            data = {'hashtagName': hashtag}
            serializer = HashtagSerializer(data=data, partial=True)
            if serializer.is_valid():
                h = serializer.save()
        hashtag_list.append(h)
    return hashtag_list


def get_old_hashtag_instances(post_hashtag_instances):
    hashtag_list = []
    for post_hashtag in post_hashtag_instances:
        hashtag_list.append(post_hashtag.hashtagId)
    return hashtag_list


def check_old_new_hashtag_instances(old_hashtag_instances, new_hashtag_instances, post_id):
    set_old_hashtag_instances = set(old_hashtag_instances)
    set_new_hashtag_instances = set(new_hashtag_instances)
    delete_post_hashtag_instance = set_old_hashtag_instances - set_new_hashtag_instances
    add_post_hashtag_instance = set_new_hashtag_instances - set_old_hashtag_instances
    for post_hashtag in delete_post_hashtag_instance:
        post_hashtag_instance = PostHashtag.objects.filter(postId=post_id).filter(hashtagId=post_hashtag)[0]
        post_hashtag_instance.delete()
    for post_hashtag in add_post_hashtag_instance:
        data = {'postId': post_id, 'hashtagId': post_hashtag.hashtagId}
        serializer = PostHashtagSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()


def delete_old_tagged_ids(post_id):
    post_tag_ids = PostTag.objects.filter(postId=post_id)
    for post_tag in post_tag_ids:
        post_tag.delete()


def update_post_description(post_description, post_id):
    new_hashtags = get_hashtags(post_description)
    new_hashtag_instances = get_new_hashtag_instances(new_hashtags)
    old_hashtag_instances = get_old_hashtag_instances(PostHashtag.objects.filter(postId=post_id))
    check_old_new_hashtag_instances(old_hashtag_instances, new_hashtag_instances, post_id)
    delete_old_tagged_ids(post_id)
    new_tagged_ids = get_tagged_ids(post_description)
    create_post_tag_instance(new_tagged_ids, post_id)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request):
    data = {}
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post = UserPost.objects.get(postId=request.data['postId'])
    if post.userProfileId == user_profile:
        if post.postDescription != request.data['postDescription']:
            data['postDescription'] = request.data['postDescription']
            update_post_description(data['postDescription'], post.id)
            post_serializer = UserPostSerializer(post, data=data, partial=True)
            if post_serializer.is_valid():
                post_serializer.save()
                return Response(post_serializer.data)
            else:
                return Response(post_serializer.errors)
        else:
            return Response(UserPostSerializer(post).data)
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_like_count(request):
    post = UserPost.objects.get(postId=request.GET['postId'])
    like_count = PostLike.objects.filter(postId=post).count()
    return Response(like_count)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_post(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post = UserPost.objects.get(postId=request.data['postId'])
    post_like = PostLike.objects.filter(postId=post).filter(userProfileId=user_profile)
    post_like[0].delete()
    return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_comment(request):
    data = {}
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    post = UserPost.objects.get(postId=request.data['postId'])
    data['userProfileId'] = user_profile.id
    data['postId'] = post.id
    data['commentDescription'] = request.data['commentDescription']
    serializer = PostCommentSerializer(data=data, partial=True)
    if serializer.is_valid():
        post_comment_instance = serializer.save()
        dic = {}
        user_profile = post_comment_instance.userProfileId
        profile_serializer = SmallDataUserProfileSerializer(user_profile)
        dic.update(profile_serializer.data)
        account_serializer = SmallDataAccountSerializer(user_profile.userId)
        dic.update(account_serializer.data)
        dic.update(serializer.data)
        return Response(dic)
    else:
        return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_comment_count(request):
    post = UserPost.objects.get(postId=request.GET['postId'])
    comment_count = PostComment.objects.filter(postId=post.id).count()
    return Response(comment_count)


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


def sort_by_time(data):
    return pd.DataFrame(data).sort_values(by='postTime').to_dict('records')[::-1]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feeds(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    followers = UserRelationship.objects.filter(followerId=user_profile).filter(relationshipStatus=1)
    user_profile_list = []
    for f in followers:
        user_profile_list.append(f.followingId)
    user_profile_list.append(user_profile)
    print(user_profile_list)
    data = []
    for user in user_profile_list:
        account_serializer = SmallDataAccountSerializer(user.userId)
        post_list = UserPost.objects.filter(userProfileId=user)
        print(post_list)
        post_serializer = UserPostSerializer(post_list, many=True)
        if not post_serializer.data:
            print(1)
            continue
        else:
            for serializer in post_serializer.data:
                dic = {}
                dic.update(account_serializer.data)
                dic.update(serializer)
                liked_post = PostLike.objects.filter(postId=UserPost.objects.get(postId=serializer['postId']))\
                    .filter(userProfileId=user_profile)
                print(liked_post, serializer['postId'])
                if liked_post:
                    dic['liked'] = True
                else:
                    dic['liked'] = False
                data.append(dic)
    if not data:
        return Response(data)
    data = sort_by_time(data)
    if len(data) > 15:
        data = data[:15]
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_a_post_detail(request):
    post_dic = {}
    post_id = request.GET['postId']
    post = UserPost.objects.get(postId=post_id)
    serializer = UserPostSerializer(post)
    post_dic.update(serializer.data)
    post_likes = PostLike.objects.filter(postId=post).count()
    post_dic['postLikes'] = post_likes
    post_dic['postComments'] = PostComment.objects.filter(postId=post).count()
    return Response(post_dic)


def sort_by_time_likes(data):
    return pd.DataFrame(data).sort_values(by='likeTime').to_dict('records')[::-1]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_likes_on_a_post(request):
    post_id = request.GET['postId']
    post = UserPost.objects.get(postId=post_id)
    post_likes = PostLike.objects.filter(postId=post)
    lst = []
    for post_like in post_likes:
        dic = {}
        user_profile = post_like.userProfileId
        serializer = SmallDataUserProfileSerializer(user_profile)
        dic.update(serializer.data)
        dic['userId'] = user_profile.userId.userid
        dic['userName'] = user_profile.userId.name
        dic['likeTime'] = post_like.likeTime
        lst.append(dic)
    lst = sort_by_time_likes(lst)
    return Response(lst)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_comments_on_a_post(request):
    post_id = request.GET['postId']
    post = UserPost.objects.get(postId=post_id)
    post_comments = PostComment.objects.filter(postId=post)
    lst = []
    for post_comment_instance in post_comments:
        dic = {}
        user_profile = post_comment_instance.userProfileId
        profile_serializer = SmallDataUserProfileSerializer(user_profile)
        dic.update(profile_serializer.data)
        comment_serializer = PostCommentSerializer(post_comment_instance)
        dic.update(comment_serializer.data)
        account_serializer = SmallDataAccountSerializer(user_profile.userId)
        dic.update(account_serializer.data)
        lst.append(dic)
    return Response(lst)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_no_of_posts(request):
    requested_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    no_of_posts = UserPost.objects.filter(userProfileId=requested_profile).count()
    return Response(no_of_posts)
