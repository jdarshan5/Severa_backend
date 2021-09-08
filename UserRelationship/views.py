from rest_framework.response import Response

from UserRelationship.models import UserRelationship
from UserRelationship.serializers import UserRelationshipSerializer

from UserProfiles.models import UserProfile
from UserProfiles.serializers import SmallDataUserProfileSerializer

from ProfileSetting.models import UserSetting

from Account.models import Account
from Account.serializers import SmallDataAccountSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from fcm_django.models import FCMDevice

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_relationship(request):
    """
    Get a relationship status like whether there exists a relation or not or it is blocked, declined, canceled etc.
    This view just gives us the info of a relationship.
    :param request:
    :return:
    """
    user_profile = UserProfile.objects.get(userId=request.user)
    requested_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)
    serializer = UserRelationshipSerializer(relation)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_relationship(request):
    """
    View is used to make a request for a relation.
    :param request:
    :return:
    """
    data = {}
    user_profile = UserProfile.objects.get(userId=request.user)
    data['followerId'] = user_profile.id
    print(request.POST.get('requested', ''))
    try:
        requested_profile = UserProfile.objects.get(userProfileId=request.POST.get('requested', ''))
        data['followingId'] = requested_profile.id
    except UserProfile.DoesNotExist:
        return Response({'Error': 'DoesNotExist'})
    relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)
    requested_profile_setting = UserSetting.objects.get(userProfile=requested_profile.id)
    if not relation:
        if requested_profile_setting.protected == 0:
            data['relationshipStatus'] = 1
            serializer = UserRelationshipSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                requested_profile_devices = FCMDevice.objects.filter(user=requested_profile.userid)
                for device in requested_profile_devices:
                    device.send_message(title='Profile Request',
                                        body=user_profile.userid.name + ' Started Following You.')
                return Response(serializer.data)
        else:
            data['relationshipStatus'] = 2
            serializer = UserRelationshipSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                requested_profile_devices = FCMDevice.objects.filter(user=requested_profile.userid)
                for device in requested_profile_devices:
                    device.send_message(title='Profile Request',
                                        body=user_profile.userid.name + ' Has Sent You A Request.')
                return Response(serializer.data)
    else:
        if relation[0].relationshipStatus == 1:
            return Response({'relation': 'Already accepted.'})
        elif relation[0].relationshipStatus == 2:
            if requested_profile_setting.protected == 0:
                data['relationshipStatus'] = 1
                serializer = UserRelationshipSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    requested_profile_devices = FCMDevice.objects.filter(user=requested_profile.userid)
                    for device in requested_profile_devices:
                        device.send_message(title='Profile Request',
                                            body=user_profile.userid.name + ' Started Following You.')
                    return Response(serializer.data)
            else:
                data['relationshipStatus'] = 0
                serializer = UserRelationshipSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
        elif relation[0].relationshipStatus == 3:
            return Response({'relation': 'prohibited'})
    return Response({})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_following_relationships(request):
    """
    Get all the followings of a user.
    :param request:
    :return:
    """
    lst = []
    user_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    user_relationship = UserRelationship.objects.filter(followerId=user_profile).filter(relationshipStatus=1)
    for r in user_relationship:
        data = {}
        follower_account = r.followingId.userId
        follower_profile = r.followingId
        account_serializer = SmallDataAccountSerializer(follower_account)
        data.update(account_serializer.data)
        profile_serializer = SmallDataUserProfileSerializer(follower_profile)
        data.update(profile_serializer.data)
        lst.append(data)
    return Response(lst)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_follower_relationships(request):
    """
    Get all the followers of a user.
    :param request:
    :return:
    """
    lst = []
    user_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    user_relationship = UserRelationship.objects.filter(followingId=user_profile).filter(relationshipStatus=1)
    for r in user_relationship:
        data = {}
        follower_account = r.followerId.userId
        follower_profile = r.followerId
        account_serializer = SmallDataAccountSerializer(follower_account)
        data.update(account_serializer.data)
        profile_serializer = SmallDataUserProfileSerializer(follower_profile)
        data.update(profile_serializer.data)
        lst.append(data)
    return Response(lst)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_relationships(request):
    """
    Get all the pending requests of a user.
    :param request:
    :return:
    """
    user_profile = UserProfile.objects.get(userId=request.user)
    relation = UserRelationship.objects.filter(followerId=user_profile).filter(relationshipStatus=0)
    serializer = UserRelationshipSerializer(relation, many=True)
    return Response(serializer.data)


def following_count_value(user_profile_id, following=True):
    try:
        user_profile = UserProfile.objects.get(userProfileId=user_profile_id)
    except UserProfile.DoesNotExist:
        return None
    if following:
        return UserRelationship.objects.filter(followerId=user_profile).filter(relationshipStatus=1).count()
    else:
        return UserRelationship.objects.filter(followingId=user_profile).filter(relationshipStatus=1).count()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_count(request):
    """
    Get no. of followings of a user.
    :param request:
    :return:
    """
    # data = {'followings': following_count_value(request.GET['requested'])}
    user_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    data = {'followings': UserRelationship.objects.filter(followerId=user_profile).filter(relationshipStatus=1).count()}
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def follower_count(request):
    """Get no. of followers of a user.
    :param request:
    :return:
    """
    # data = {'followers': following_count_value(request.GET['requested'], following=False)}
    user_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    data = {'followers': UserRelationship.objects.filter(followingId=user_profile).filter(relationshipStatus=1).count()}
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def block_relation(request):
    """
    Used to block someone.
    :param request:
    :return:
    """
    data = {}
    user_profile = UserProfile.objects.get(userId=request.user)
    requested_profile = UserProfile.objects.get(userProfileId=request.POST['requested'])
    relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)
    if not relation:
        data['followerId'] = user_profile
        data['followingId'] = requested_profile
        data['relationshipStatus'] = 3
        serializer = UserRelationshipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            requested_relation = \
                UserRelationship.objects.filter(follower_count=requested_profile).filter(followingId=user_profile)
            if not requested_profile:
                pass
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        if relation[0].relationshipStatus != 3:
            serializer = UserRelationshipSerializer(relation, data={'relationshipStatus': 3}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_relationship(request):
    """
    Used to refuse a relation.
    :param request:
    :return:
    """
    user_profile = UserProfile.objects.get(userId=request.user)
    requested_profile = UserProfile.objects.get(userProfileId=request.POST['requested'])
    relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)[0]
    if relation.relationshipStatus == 0:
        serializer = UserRelationshipSerializer(relation, data={'relationshipStatus': 4}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_relationship(request):
    """
    Used to accept a pending relationship.
    :param request:
    :return:
    """
    user_profile = UserProfile.objects.get(userId=request.user)
    requested_profile = UserProfile.objects.get(userProfileId=request.POST['requested'])
    relation = UserRelationship.objects.filter(followerId=requested_profile).filter(followingId=user_profile)[0]
    if relation.relationshipStatus == 0:
        serializer = UserRelationshipSerializer(relation, data={'relationshipStatus': 1}, partial=True)
        if serializer.is_valid():
            serializer.save()
            requested_profile_devices = FCMDevice.objects.filter(user=requested_profile.userid)
            for device in requested_profile_devices:
                device.send_message(title='Profile Request',
                                    body=user_profile.userid.name + ' Has Accepted Your Request.')
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_relationship(request):
    user_profile = UserProfile.objects.get(userId=request.user)
    requested_profile = UserProfile.objects.get(userProfileId=request.POST['requested'])
    relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)[0]
    if relation.relationshipStatus == 1:
        serializer = UserRelationshipSerializer(relation, data={'relationshipStatus': 2}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    return Response({})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_followings(request):
    # user_profile = UserProfile.objects.get(userId=request.user)
    requested_accounts = Account.objects.filter(userid__contains=request.GET.get('user_id', ''))
    profile_data = []
    for account in requested_accounts:
        data = {}
        account_serializer = SmallDataAccountSerializer(account)
        data.update(account_serializer.data)
        profile = UserProfile.objects.get(userId=account)
        profile_serializer = SmallDataUserProfileSerializer(profile)
        data.update(profile_serializer.data)
        profile_data.append(data)
    return Response(profile_data)
    # profiles = UserRelationship.objects.filter(followerId=user_profile).filter(followingId__in=requested_profiles)
    # serializer = SmallDataUserProfileSerializer(profiles, many=True)
    # return Response(serializer.data)
