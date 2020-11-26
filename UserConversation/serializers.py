from rest_framework import serializers
from .models import UserConversation, UserMessages, SharedFile


class UserConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConversation
        fields = ['conversationId', 'messageSender', 'messageReceiver']


class UserMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessages
        fields = ['conversationId', 'messageSentTime', 'messageReceivedTime', 'messageReference', 'messageContent',
                  'messageTypeExtension', 'messageStatus']


class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ['referenceId', 'data']
