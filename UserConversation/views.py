from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from UserProfiles.models import UserProfile

from UserConversation.models import UserConversation, UserMessages, SharedFile

from UserConversation.serializers import UserConversationSerializer, UserMessagesSerializer, SharedFileSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    msg_to_profile = UserProfile.objects.get(userProfileId=request.data['msgToId'])
    conversation = UserConversation.objects.filter(messageSender=user_profile).filter(messageReceiver=msg_to_profile)
    if not conversation:
        data = {'messageSender': user_profile.id, 'messageReceiver': msg_to_profile.id}
        conversation_serializer = UserConversationSerializer(data=data)
        if conversation_serializer.is_valid():
            conversation = conversation_serializer.save()
            msg_data = {'conversationId': conversation.id, 'messageType': request.data['messageType']}
            if msg_data['messageType'] == 0 or msg_data['messageType'] == 2:
                msg_data['messageContent'] = request.data['messageContent']
            elif msg_data['messageType'] == 1:
                shared_file_data = {'data': request.data['messageContent']}
                shared_file_serializer = SharedFileSerializer(data=shared_file_data)
                if shared_file_serializer.is_valid():
                    shared_file = shared_file_serializer.save()
                    msg_data['messageContent'] = shared_file.referenceId
            user_message_serializer = UserMessagesSerializer(data=msg_data)
            if user_message_serializer.is_valid():
                user_message_serializer.save()
                return Response(user_message_serializer.data)
            else:
                return Response(user_message_serializer.errors)
        else:
            return Response(conversation_serializer.errors)
    else:
        data = {'conversationId': conversation[0].id, 'messageType': request.data['messageType'],
                'messageContent': request.data['messageContent']}
        if int(data['messageType']) == 2:
            shared_file_data = {'data': request.data['messageContent']}
            shared_file_serializer = SharedFileSerializer(data=shared_file_data)
            if shared_file_serializer.is_valid():
                shared_file = shared_file_serializer.save()
                data['messageContent'] = str(shared_file.referenceId)
            else:
                return Response(shared_file_serializer.errors)
        user_message_serializer = UserMessagesSerializer(data=data)
        if user_message_serializer.is_valid():
            user_message_serializer.save()
            return Response(user_message_serializer.data)
        else:
            return Response(user_message_serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_conversation(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_a_message(request):
    pass
