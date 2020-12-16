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
    conversationId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    messageSender = models.ForeignKey(UserProfile,
                                      on_delete=models.DO_NOTHING,
                                      related_name='userProfileIdOfTheMessageSender')
    messageReceiver = models.ForeignKey(UserProfile,
                                        on_delete=models.DO_NOTHING,
                                        related_name='userProfileIdOfTheMessageReceiver')

    def __str__(self):
        return str(self.messageSender) + " >>> " + str(self.messageReceiver)


class UserMessages(models.Model):
    """
    Table contains all the messages in a conversation between two users.
    conversationId        : Conversation id for two users.               E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    messageSentTime       : Time when the sender sends the message.      E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    messageReceivedTime   : Time when the receiver receives the message. E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    messageType           : Type of the message.                         E.g.: 0-Text, 1-Photo, 1-Video, 1-Audio, 2-Shared Post
    messageContent        : Binary data of the Message.                  E.g.: For text, simple text data will be stored,
        For Image, Video, a referenceId will be stored in the filed E.g.: a uuid
        For post, a uuid of the post will be stored
    messageStatus         : Status whether the msg is read or not        E.g.: 0-read, 1-unread
    messageReadTime       : What was the time when the user who received the msg read it.
    """
    conversationId = models.ForeignKey(UserConversation, on_delete=models.DO_NOTHING)
    messageId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    messageSentTime = models.DateTimeField(auto_now_add=True)
    messageReceivedTime = models.DateTimeField(blank=True, null=True)
    messageType = models.IntegerField(default=0)
    messageContent = models.TextField()
    messageStatus = models.IntegerField(default=1)
    messageReadTime = models.DateTimeField(blank=True, null=True)


class SharedFile(models.Model):
    """
    Table is used to store all the media (image, video, audio) which is shared to in a Conversation.
    referenceId        : Unique id.
    data               : File which got shared in a conversation.
    """
    referenceId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    data = models.FileField(upload_to='SharedFile/', null=False)
