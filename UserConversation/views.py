from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from UserProfiles.models import UserProfile

from UserConversation.models import UserConversation, UserMessages

from UserConversation.serializers import UserConversationSerializer, UserMessagesSerializer, SharedFileSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    msg_to_profile = UserProfile.objects.get(userId=request.data['msgToId'])
    conversation = UserConversation.objects.filter(messageSender=user_profile).filter(messageReceiver=msg_to_profile)
    if not conversation:
        data = {'messageSender': user_profile, 'messageReceiver': msg_to_profile}
        conversation_serializer = UserConversationSerializer(data=data)
        if conversation_serializer.is_valid():
            conversation = conversation_serializer.save()
            msg_data = {'conversationId': conversation, 'messageType': request.data['messageType']}
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
        data = {'conversationId': conversation[0], 'messageType': request.data['messageType']}
        if data['messageType'] == 0 or data['messageType'] == 1:
            data['messageContent'] = request.data['messageContent']
        elif data['messageType'] == 2:
            shared_file_data = {'data': request.data['messageContent']}
            shared_file_serializer = SharedFileSerializer(data=shared_file_data)
            if shared_file_serializer.is_valid():
                shared_file = shared_file_serializer.save()
                data['messageContent'] = shared_file.referenceId
        user_message_serializer = UserMessagesSerializer(data=data)
        if user_message_serializer.is_valid():
            user_message_serializer.save()
            return Response(user_message_serializer.data)
    return Response({})
