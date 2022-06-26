from posts.models import PostLikes
from .models import Profile
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404

def get_avatar(request):


    if not request.user.is_authenticated or request.user is AnonymousUser:
        return dict(get_avatar=None)
    user = request.user
    userprofile = Profile.objects.filter(user=user).first()
    avatar = userprofile.profile_picture.url
    return dict(get_avatar=avatar)


def get_liked_posts_by_user(request):
    
    if not request.user.is_authenticated or request.user is AnonymousUser:
        return dict(get_liked_posts_by_user=None)
    user = request.user
    print("user=",user)
    #userprofile = Profile.objects.filter(user=user).first()
    userprofile  = get_object_or_404(Profile, user=user)
    print("userprofile=", userprofile)
    posts_liked = userprofile.get_all_liked_posts()
    print("posts_liked=", posts_liked)
    

    return {"posts_liked": posts_liked}