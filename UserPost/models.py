from django.db import models

from UserProfiles.models import UserProfile
from Hashtags.models import Hashtag

import uuid

# Create your models here.


class UserPost(models.Model):
    """
    Table containing all the information about a post when User posts.
    userProfileId      : Unique Id for all the users.            E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    postId             : Unique Id for the Post.                 E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    postContent        : Binary data of the post.                E.g.: 0-Binary data of image, 1-Binary data of Video
    postDescription    : Description of the post.                E.g.: Sun sines.
    postTime           : Time at which media was posted.         E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    postLocation       : Coordinates of the Location.            E.g.: [Latitude, Longitude]:[23.020708, 72.515868]
    postStatus         : Status of the post.                     E.g.: 0-Active, 1-Blocked, 2-Reported
    """
    userProfileId = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    postId = models.UUIDField(default=uuid.uuid4, editable=False)
    postContent = models.FileField(upload_to='UserPost/', null=False)
    postDescription = models.TextField(null=True, blank=True)
    postTime = models.DateTimeField(auto_now_add=True)
    postStatus = models.IntegerField(default=0)

    def __str__(self):
        return str(self.userProfileId) + ' - ' + str(self.postId)


class PostLike(models.Model):
    """
    Table containing all the likes on the posts.
    userProfileId      : Id of the user who liked the post.      E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    postId             : Unique Id for the Post.                 E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    likeTime           : Time at which user liked Post.          E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    """
    userProfileId = models.ForeignKey(UserProfile,
                                      on_delete=models.CASCADE,
                                      related_name='userProfileIdOfTheUserWhoLiked')
    postId = models.ForeignKey(UserPost,
                               on_delete=models.CASCADE,
                               related_name='postIdOfThePostWhichGotLiked')
    likeTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.postId)


class PostComment(models.Model):
    """
    Table containing all the comments on the post.
    userProfileId      : Id of the user who commented.           E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    postId             : Unique Id for the Post.                 E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    commentId          : Unique Id for the Comment.              E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    commentDescription : Comment of a particular user.           E.g.: Nice Click.
    commentTime        : Time at which user commented on Post.   E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    commentStatus      : Status of the comment.                  E.g.: 0-Active, 1-Blocked, 2-Reported
    """
    userProfileId = models.ForeignKey(UserProfile,
                                      on_delete=models.CASCADE,
                                      related_name='userProfileIdOfTheUserWhoCommented')
    postId = models.ForeignKey(UserPost,
                               on_delete=models.CASCADE,
                               related_name='postIdOfThePostWhichGotCommented')
    commentId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commentDescription = models.TextField(blank=False, null=False)
    commentTime = models.DateTimeField(auto_now_add=True)
    commentStatus = models.IntegerField(default=0)


class PostSubComment(models.Model):
    """
    Table containing all the sub comments of a comment.
    postId             : Unique Id for the Post.                 E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    subCommentId       : Unique Id for the Comment.              E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    commentDescription : Comment of a particular user.           E.g.: Nice Click.
    commentTime        : Time at which user commented on Post.   E.g.: datetime.datetime(2020, 10, 18, 19, 39, 6, 507584)
    commentStatus      : Status of the comment.                  E.g.: 0-Active, 1-Blocked, 2-Reported
    """
    userProfileId = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parentComment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    subCommentId = models.UUIDField(default=uuid.uuid4, editable=False)
    commentDescription = models.TextField(blank=False, null=False)
    commentTime = models.DateTimeField(auto_now_add=True)
    commentStatus = models.IntegerField(default=0)


class PostTag(models.Model):
    """
    Table containing all the tags of the user of a post.
    userProfileId      : Id of the user who got taged.    E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    postId             : Id of the Post.                  E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    postTagId          : Unique postTag Id.               E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    """
    userProfileId = models.ForeignKey(UserProfile,
                                      on_delete=models.CASCADE,
                                      related_name='userProfileIdOfTheUserWhoGotTaggedInPost')
    postId = models.ForeignKey(UserPost,
                               on_delete=models.CASCADE,
                               related_name='postIdOfThePostWhichGotTags')
    postTagId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class PostHashtag(models.Model):
    """
    Table containing all the hashtags used in the post.
    userProfileId      : Unique Id for all the users.            E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    postId             : Unique Id for the Post.                 E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    hashtagId          : Id of the hashtag.                      E.g.: op026D49Ce5F2v80h1g97R1R13IJHQ
    """
    postId = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='postIdOfThePostWhichGotHashtag')
    hashtagId = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='hashtagIdInThePostWhichAreUsed')
