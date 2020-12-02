from rest_framework import serializers

from .models import UserProfile


class RegisterUserProfileSerializer(serializers.ModelSerializer):
    """
    This serializer class is used for the a new user's registration of UserProfile.
    """
    class Meta:
        # Model to be serialized
        model = UserProfile
        # Fields which will get serialized
        fields = ['userId', 'userProfileId', 'userProfilePicture', 'descriptionOfUser', 'userPhone']
        # Serialized read_only fields
        read_only = ['userProfileId']


class SmallDataUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer used to only fetch a user's userProfilePicture and userProfileId
    """
    class Meta:
        # Model to be serialized
        model = UserProfile
        # Fields which will get serialized
        fields = ['userProfileId', 'userProfilePicture']
        # Serialized read_only fields
        read_only = ['userProfileId']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer used to fetch all the data of a user's UserProfile.
    """
    class Meta:
        # Model to be serialized
        model = UserProfile
        # Fields which will get serialized
        fields = ['userProfileId', 'userProfilePicture', 'descriptionOfUser', 'userPhone']
        # Serialized read_only fields
        read_only = ['userProfileId']
