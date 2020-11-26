from django.db import models

from UserProfiles.models import UserProfile

import uuid

# Create your models here.


class UserRelationship(models.Model):
    """
    Table contains all the relationship between the users.
    relationshipId : Unique id of all the relations between two users. E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    followerId : A user who follows someone, contains userProfileId. E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    followingId : A user who gets followed, contains userProfileId. E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    relationshipStatus : Status of a relationship. E.g.: 0-Pending, 1-Accepted, 2-Cancel, 3-Blocked, 4-Decline, 5-Restricted
    """
    relationshipId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    followerId = models.ForeignKey(UserProfile,
                                   on_delete=models.CASCADE,
                                   related_name='userProfileIdOfTheUserWhoIsFollows')
    followingId = models.ForeignKey(UserProfile,
                                    on_delete=models.CASCADE,
                                    related_name='userProfileIdOfTheUserWhoGotFollowed')
    relationshipStatus = models.IntegerField()
    relationshipCreatedTime = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.followerId) + " ~~~ " + str(self.followingId)
