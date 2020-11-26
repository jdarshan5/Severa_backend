from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from UserProfiles.models import UserProfile

from UserConversation.models import UserConversation, UserMessages

from UserConversation.serializers import UserConversationSerializer, UserMessagesSerializer

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
            msg_data = {'conversationId': conversation, '': ''}
            UserMessagesSerializer(data=msg_data)
    else:
        pass
    return Response({})
