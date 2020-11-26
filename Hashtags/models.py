from django.db import models
import uuid

# Create your models here.


class Hashtag(models.Model):
    """
    hashtagId          : Id of the hashtag.           E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    hashtagName        : Name of the hashtag.         E.g.: candid, clicked, black, white, B&W
    """
    hashtagId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hashtagName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.hashtagName
