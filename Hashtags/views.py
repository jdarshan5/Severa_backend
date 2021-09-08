from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from Hashtags.models import Hashtag

from UserPost.models import PostHashtag

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hashtag_count(request):
    hashtag_id = request.data['hashtagId']
    hashtag = Hashtag.objects.get(hashtagId=hashtag_id)
    count = PostHashtag.objects.filter(hashtagId=hashtag).count()
    return Response(count)
