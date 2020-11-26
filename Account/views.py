from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ProfileSetting.serializers import UserSettingSerializer
from UserProfiles.serializers import RegisterUserProfileSerializer
from .serializers import RegistrationSerializer

from Account.serializers import AccountSerializer

from django.contrib.auth.hashers import check_password

# Create your views here.


@api_view(['POST', ])
def registration_view(request):
    # View to register a new user which creates an Account with userid, useremail, name(userName) and password.
    # and by this account's instance this view also creates UserProfiles object simultaneously.

    # Checking whether the request is POST request or not, if not it will automatically raise an Exception.
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        # Validating the data of the serializer before saving it.
        if serializer.is_valid():
            account = serializer.save()
            register_user_profile_serializer = RegisterUserProfileSerializer(data={'userId': account.id})
            if register_user_profile_serializer.is_valid():
                user_profile = register_user_profile_serializer.save()
                profile_setting_serializer = UserSettingSerializer(data={'userProfile': user_profile.id})
                if profile_setting_serializer.is_valid():
                    profile_setting_serializer.save()
                else:
                    return Response(profile_setting_serializer.errors)
            else:
                return Response(register_user_profile_serializer.errors)
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            return Response(serializer.errors)
        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_userid(request):
    data = {}
    user_account = request.user
    data['userid'] = request.POST['userid']
    serializer = AccountSerializer(user_account, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user_account = request.user
    current_password = user_account.password
    current_password_entered = request.POST['old_password']
    matched = check_password(current_password_entered, current_password)
    if matched:
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            return Response({'passwords must match.'})
        if not len(password) >= 8:
            return Response({'Password length not accepted. (Should be 8 or more)'})
        user_account.set_password(password)
        user_account.save()
    else:
        return Response({'Please enter correct current password.'})
    return Response({matched})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_name(request):
    data = {}
    user_account = request.user
    data['name'] = request.POST['name']
    serializer = AccountSerializer(user_account, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password(request):
    pass
