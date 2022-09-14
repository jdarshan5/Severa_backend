from UserPost.models import PostHashtag, UserPost

s = '''Here are some of the best IDEs for mobile! Which one do you use?
Original post created by @itchallenges
Follow @webdevofficial for more!
#webdev #css #webdeveloper #html #webdevelopment #javascript #coding #programming #webdesign #developer #programmer #coder #code #web #website #frontend #daysofcode #frontenddeveloper #codinglife #ui #design #programmers #webdevelopers #softwaredeveloper #php #webdesigner #ux #devlife #developerlife #bhfyp'''


def get_hashtags_s(post_description):
    pd_list = post_description.split()
    all_hashtags = []
    for value in pd_list:
        if value[0] == '#':
            all_hashtags.append(value[1:])
    return all_hashtags


post = UserPost.objects.get(postId='52770337-bce7-417a-bae1-3532b38fd143')
new_hashtags = get_hashtags_s(s)
post_hashtag_list = PostHashtag.objects.filter(postId=post.id).hashtagId
