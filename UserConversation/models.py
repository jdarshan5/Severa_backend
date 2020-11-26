from django.db import models

from UserProfiles.models import UserProfile

import uuid

# Create your models here.


class UserConversation(models.Model):
    """
    Table contains Conversation between two users.
    conversationId  : Unique conversation id for two users.   E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    messageFrom     : userProfileId of the message sender.    E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    messageReceiver : userProfileId of the message receiver.  E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    """
    conversationId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    messageSender = models.ForeignKey(UserProfile,
                                      on_delete=models.CASCADE,
                                      related_name='userProfileIdOfTheMessageSender')
    messageReceiver = models.ForeignKey(UserProfile,
                                        on_delete=models.CASCADE,
                                        related_name='userProfileIdOfTheMessageReceiver')

    def __str__(self):
        return str(self.messageSender) + " >>> " + str(self.messageReceiver)


class UserMessages(models.Model):
    """
    Table contains all the messages in a conversation between two users.
    conversationId        : Conversation id for two users.               E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    messageSentTime       : Time when the sender sends the message.      E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    messageReceivedTime   : Time when the receiver receives the message. E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    messageType           : Type of the message.                         E.g.: 0-Text, 1-Audio, 2-Photo, 3-Video
    messageContent        : Binary data of the Message.                  E.g.: Binary Data
    messageTypeExtension  : Type of the extension.                       E.g.: 0-txt, 1-mp3, 2-jpg,png, 3-mp4
    messageStatus         : Status whether the msg is read or not        E.g.: 0-read, 1-unread
    """
    conversationId = models.ForeignKey(UserConversation, on_delete=models.CASCADE)
    messageId = models.UUIDField(default=uuid.uuid4, editable=False)
    messageSentTime = models.DateTimeField(blank=True, format='%Y-%m-%d %H:%M:%S')
    messageReceivedTime = models.DateTimeField(blank=True)
    messageType = models.IntegerField(default=0)
    messageContent = models.TextField()
    messageTypeExtension = models.IntegerField(default=0)
    messageStatus = models.IntegerField(default=1)
    messageReadTime = models.DateTimeField()