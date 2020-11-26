from rest_framework import serializers
from .models import UserSetting


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        # Model to be serialized
        model = UserSetting
        fields = ['userProfile', 'profileStatus', 'profileType', 'protected']
