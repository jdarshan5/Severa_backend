from django.db import models

from UserProfiles.models import UserProfile

# Create your models here.


class UserDevice(models.Model):
    """

    """
    userProfileId = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
