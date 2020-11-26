from django.db import models
from UserProfiles.models import UserProfile

# Create your models here.


class UserSetting(models.Model):
    """
    Table containing all the settings of the user.
    userProfileId     : Unique Id of the user                   E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    accountStatus     : Status of an Account.                   E.g.: 0-Active, 1-Blocked, 2-Reported
    userType          : Type of a User.                         E.g.: 0-Normal, 1-Business
    protected         : Protection of an Account.               E.g.: 0-Public, 1-Private
    """
    userProfile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    profileStatus = models.IntegerField(default=0)
    profileType = models.IntegerField(default=0)
    protected = models.IntegerField(default=0)

    def __str__(self):
        return str(self.userProfile)
