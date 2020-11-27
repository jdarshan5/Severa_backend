from rest_framework import serializers
from .models import UserConversation, UserMessages, SharedFile


class UserConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConversation
        fields = ['conversationId', 'messageSender', 'messageReceiver']


class UserMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessages
        fields = ['conversationId', 'messageId', 'messageSentTime', 'messageReceivedTime', 'messageType',
                  'messageContent', 'messageStatus', 'messageReadTime']


class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ['referenceId', 'data']
