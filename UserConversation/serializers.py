from rest_framework import serializers
from .models import UserConversation, UserMessages


class UserConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConversation
        fields = ['conversationId', 'messageSender', 'messageReceiver']


class UserMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessages
        fields = ['conversationId', 'messageSentTime', 'messageReceivedTime', 'messageType', 'messageContent',
                  'messageTypeExtension', 'messageStatus']
