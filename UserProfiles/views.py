from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .serializers import UserProfileSerializer, SmallDataUserProfileSerializer

from Account.models import Account
from Account.serializers import AccountSerializer, SmallDataAccountSerializer

from UserRelationship.models import UserRelationship

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_profiles(request):
    profile_data = []
    try:
        account_list = Account.objects.filter(userid__contains=request.GET['user_id'])
    except UserProfile.DoesNotExist:
        data = {'Error': 'UserId does not exist.'}
        return Response(data)
    for account in account_list:
        data = {}
        account_serializer = SmallDataAccountSerializer(account)
        data.update(account_serializer.data)
        profile = UserProfile.objects.get(userId=account)
        profile_serializer = SmallDataUserProfileSerializer(profile)
        data.update(profile_serializer.data)
        profile_data.append(data)
    return Response(profile_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_small_profile_by_id(request):
    profile_data = {}
    try:
        requested_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    except Account.DoesNotExist:
        return Response({'profile_error': 'account_does_not_exist'})
    account_serializer = SmallDataAccountSerializer(requested_profile.userId)
    profile_data.update(account_serializer.data)
    profile_serializer = SmallDataUserProfileSerializer(requested_profile)
    profile_data.update(profile_serializer.data)
    return Response(profile_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_full_profile_by_id(request):
    profile_data = {}
    user_profile = UserProfile.objects.get(userId=request.user)
    requested_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    requested_account = requested_profile.userId
    account_serializer = AccountSerializer(requested_account)
    profile_serializer = UserProfileSerializer(requested_profile)
    profile_data.update(account_serializer.data)
    profile_data.update(profile_serializer.data)
    relation = UserRelationship.objects.filter(followerId=user_profile).filter(followingId=requested_profile)
    if not relation:
        profile_data['relation'] = None
    else:
        relation = relation[0].relationshipStatus
        if relation == 3:
            return Response({})
        profile_data['relation'] = relation
    return Response(profile_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_profiles(request):
    profile_data = []
    account_list = Account.objects.all()
    for account in account_list:
        data = {}
        account_serializer = SmallDataAccountSerializer(account)
        data.update(account_serializer.data)
        profile = UserProfile.objects.get(userId=account)
        profile_serializer = SmallDataUserProfileSerializer(profile)
        data.update(profile_serializer.data)
        profile_data.append(data)
    return Response(profile_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_profile_picture(request):
    data = {}
    user_profile = UserProfile.objects.get(userId=request.user)
    data['userProfilePicture'] = request.FILES['change_profile_picture']
    serializer = UserProfileSerializer(user_profile, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_profile_description(request):
    data = {}
    user_profile = UserProfile.objects.get(userId=request.user)
    data['descriptionOfUser'] = request.data['change_profile_description']
    serializer = UserProfileSerializer(user_profile, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_id(request):
    data = {}
    user_profile = UserProfile.objects.get(userId=request.user)
    data['userProfileId'] = user_profile.userProfileId
    return Response(data)
