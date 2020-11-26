from rest_framework import serializers
from .models import UserRelationship


class UserRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelationship
        fields = ['relationshipId', 'followerId', 'followingId', 'relationshipStatus', 'relationshipCreatedTime']
