from django.db import models
from UserProfiles.models import UserProfile
from Hashtags.models import Hashtag
import uuid

# Create your models here.


class UserMoment(models.Model):
    """
    userProfileId         : userProfileId of the user who post Moment.    E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    momentId              : Unique moment Id for each moment.             E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    momentType            : Type of the moment.                           E.g.: 0-Photo, 1-Video
    momentTypeExtension   : Type of Extension of the moment.              E.g.: 0-jpg,png, 1-mp4
    momentContent         : Binary Content of the Moment.                 E.g.: Binary data
    momentTime            : Time of the moment Posted.                    E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    momentLocation        : Location of the moment.                       E.g.: [Latitude, Longitude]:[23.020708, 72.515868]
    momentStatus          : Status of the moment.                         E.g.: 0-Active, 1-Blocked, 2-Reported
    """
    userProfileId = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    momentId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    momentType = models.IntegerField()
    momentTypeExtension = models.IntegerField()
    momentContent = models.BinaryField()
    momentTime = models.DateTimeField(auto_now_add=True)
    # momentLocation = models.LocationField()
    momentStatus = models.IntegerField(default=0)


class MomentTags(models.Model):
    """
    userProfileId         : userProfileId of the user who got tagged in Moment.    E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    momentId              : Unique moment Id for each moment.                      E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    momentTagId           : Unique momentTag Id.                                   E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    """
    userProfileId = models.ForeignKey(UserProfile,
                                      on_delete=models.CASCADE,
                                      related_name='userProfileIdOfTheUserWhoGotTagged')
    momentId = models.ForeignKey(UserMoment,
                                 on_delete=models.CASCADE,
                                 related_name='IdOfTheMomentInWhichUserGotTagged')
    momentTagId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class MomentHashtags(models.Model):
    """
    momentId              : Unique moment Id for each moment.                      E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    hashtagId             : Id of the hashtag.                                     E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    """
    momentId = models.ForeignKey(UserMoment,
                                 on_delete=models.CASCADE,
                                 related_name='momentIdOfTheMomentInWhichHashtagUsed')
    hashtagId = models.ForeignKey(Hashtag,
                                  on_delete=models.CASCADE,
                                  related_name='hashtagIdOfTheHashtagUsedInMoment')
