from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from UserProfiles.models import UserProfile

from .models import UserSetting
from .serializers import UserSettingSerializer

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_setting(request):
    requested_profile = UserProfile.objects.get(userProfileId=request.GET['requested'])
    requested_profile_setting = UserSetting.objects.get(userProfile=requested_profile)
    serializer = UserSettingSerializer(requested_profile_setting)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def alter_profile_protection(request):
    data = {}
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    profile_setting = UserSetting.objects.get(userProfile=user_profile)
    if profile_setting.protected == 0:
        data['protected'] = 1
        serializer = UserSettingSerializer(profile_setting, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    data['protected'] = 0
    serializer = UserSettingSerializer(profile_setting, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)
