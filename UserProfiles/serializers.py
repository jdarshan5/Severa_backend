from rest_framework import serializers
from .models import UserProfile


class RegisterUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        # Model to be serialized
        model = UserProfile
        # Fields which will get serialized
        fields = ['userId', 'userProfileId', 'userProfilePicture', 'descriptionOfUser', 'userPhone']
        # Serialized read_only fields
        read_only = ['userProfileId']


class SmallDataUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # Model to be serialized
        model = UserProfile
        # Fields which will get serialized
        fields = ['userProfileId', 'userProfilePicture']
        # Serialized read_only fields
        read_only = ['userProfileId']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        # Model to be serialized
        model = UserProfile
        # Fields which will get serialized
        fields = ['userProfileId', 'userProfilePicture', 'descriptionOfUser', 'userPhone']
        # Serialized read_only fields
        read_only = ['userProfileId']
