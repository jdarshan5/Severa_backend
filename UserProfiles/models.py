from django.db import models
from Account.models import Account

import uuid

# Create your models here.


class UserProfile(models.Model):
    """
    userId            : Unique Id of the user.                  E.g.: @darshan_javiya
    userProfileId     : Unique Id for all the users.            E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    userProfilePicture: Profile picture of the user.
    descriptionOfUser : Information about a user of his choice.
    userPhone         : Phone number of the user.               E.g.: 1234567890
    """
    userId = models.OneToOneField(Account, on_delete=models.CASCADE, unique=True, null=False)
    userProfileId = models.UUIDField(default=uuid.uuid4, editable=False)
    userProfilePicture = models.ImageField(upload_to='UserProfile/', null=True, blank=True)
    descriptionOfUser = models.TextField(null=True, blank=True)
    userPhone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.userId)
