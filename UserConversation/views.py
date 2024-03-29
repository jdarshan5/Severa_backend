from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from UserProfiles.models import UserProfile

from UserConversation.models import UserConversation, UserMessages, SharedFile

from UserConversation.serializers import UserConversationSerializer, UserMessagesSerializer, SharedFileSerializer

from datetime import datetime

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    msg_to_profile = UserProfile.objects.get(userProfileId=request.data['messageToId'])
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
def get_messages_between_two_user(request):
    lst = []
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    conversation_id1 = request.data['conversationId1']
    conversation_id2 = request.data['conversationId2']
    conversation1 = UserConversation.objects.get(conversationId=conversation_id1)
    conversation2 = UserConversation.objects.get(conversationId=conversation_id2)
    # conversation1_serializer = UserConversationSerializer(conversation1)
    # conversation2_serializer = UserConversationSerializer(conversation2)
    conversation1_messages = UserMessages.objects.filter(conversationId=conversation1)
    conversation2_messages = UserMessages.objects.filter(conversationId=conversation2)
    message1_serializer = UserMessagesSerializer(conversation1_messages, many=True)
    message2_serializer = UserMessagesSerializer(conversation2_messages, many=True)
    # messages_1 = np.array(message1_serializer.data)
    # messages_2 = np.array(message2_serializer.data)
    for msg in message1_serializer.data:
        dic = {'userProfileId': user_profile.userProfileId,
               'conversationId': msg['conversationId'],
               'messageId': msg['messageId'],
               'messageSentTime': msg['messageSentTime'],
               'messageReceivedTime': msg['messageReceivedTime'],
               'messageType': msg['messageType'],
               'messageContent': msg['messageContent'],
               'messageStatus': msg['messageStatus'],
               'messageReadTime': msg['messageReadTime']}
        lst.append(dic)
    for msg in message2_serializer.data:
        dic = {'userProfileId': user_profile.userProfileId,
               'conversationId': msg['conversationId'],
               'messageId': msg['messageId'],
               'messageSentTime': msg['messageSentTime'],
               'messageReceivedTime': msg['messageReceivedTime'],
               'messageType': msg['messageType'],
               'messageContent': msg['messageContent'],
               'messageStatus': msg['messageStatus'],
               'messageReadTime': msg['messageReadTime']}
        lst.append(dic)
    lst.sort(key=lambda val: val['messageSentTime'], reverse=True)
    return Response(lst)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_a_message(request):
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    message_id = request.POST['messageId']
    conversation_id = request.POST['conversationId']
    conversation = UserConversation.objects.filter(messageSender=user_profile).filter(conversationId=conversation_id)
    message = UserMessages.objects.filter(conversationId=conversation[0]).filter(messageId=message_id)
    message[0].delete()
    return Response({'status': 'success'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_of_conversation(request):
    """
    This view is used to get all the list of conversation a user have.
    :param request:
    :return:
    """
    user_account = request.user
    user_profile = UserProfile.objects.get(userId=user_account)
    conversation = UserConversation.objects.filter(messageSender=user_profile)
    serializer = UserConversationSerializer(conversation, many=True)
    return Response(serializer.data)


def date_time_object_from_time_stamp(time_stamp):
    return datetime.fromtimestamp(time_stamp)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def message_received(request):
    message_id = request.data['messageId']
    conversation_id = request.data['conversationId']
    received_time = date_time_object_from_time_stamp(int(request.data['timeStamp']))
    conversation = UserConversation.objects.get(conversationId=conversation_id)
    message = UserMessages.objects.filter(conversationId=conversation).filter(messageId=message_id)[0]
    message_serializer = UserMessagesSerializer(message, data={'messageReceivedTime': received_time}, partial=True)
    if message_serializer.is_valid():
        message_serializer.save()
    else:
        return Response(message_serializer.errors)
    return Response(message_serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def message_read(request):
    message_id = request.data['messageId']
    conversation_id = request.data['conversationId']
    read_time = date_time_object_from_time_stamp(int(request.data['timeStamp']))
    conversation = UserConversation.objects.get(conversationId=conversation_id)
    message = UserMessages.objects.filter(conversationId=conversation).filter(messageId=message_id)[0]
    message_serializer = UserMessagesSerializer(message, data={'messageReadTime': read_time}, partial=True)
    if message_serializer.is_valid():
        message_serializer.save()
    else:
        return Response(message_serializer.errors)
    return Response(message_serializer.data)
