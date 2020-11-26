from rest_framework import serializers
from .models import UserMoment, MomentTags, MomentHashtags


class UserMomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMoment
        fields = ['userProfileId', 'momentId', 'momentType', 'momentTypeExtension', 'momentContent', 'momentTime',
                  'momentStatus']


class MomentTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MomentTags
        fields = ['userProfileId', 'momentId', 'momentTagId']


class MomentHashtagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MomentHashtags
        fields = ['momentId', 'hashtagId']
