from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from posts.models import Post, PostLikes


class Profile(models.Model):

    class Meta:
        #カテゴリ
        verbose_name =('ユーザプロファイル')
        verbose_name_plural = ("ユーザプロファイル")
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    profile_picture = models.ImageField(blank=True, upload_to='userprofile', null=True)
    username_slug = models.SlugField(max_length=50, default="")
    display_name = models.CharField(verbose_name="表示名", max_length=20,blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    """
    def save(self, *args, **kwargs):
        if not self.username_slug:
            #slug設定がない場合のみ自動設定
            print("slugがよばれたよ")
            self.username_slug = slugify(self.user.username)
            super(Profile, self).save(*args, **kwargs)
    """ 

    def followers_count(self):
        profile = Profile.objects.get(pk=self.pk)
        followers = int(profile.followed_by.count()) - 1  #自分自身も含まれるため-1する
        return followers


    def following_count(self):
        profile = Profile.objects.get(pk=self.pk)
        following = int(profile.follows.count()) - 1   #自分自身も含まれるため-1する
        return following
    

    def get_profile(self):
        profile = Profile.objects.get(pk=self.pk)
        return profile

    def posts_count(self):
        print("self.pk=", self.pk, "self.user.username=", self.user.username)
        posts = Post.objects.filter(owner=self.user.pk).count()
        return posts

    def get_all_liked_posts(self):
        #自分がいいねした投稿のPostデータのPKリストを取得
        list_of_id_posts_liked = list(PostLikes.objects.filter(user=self.user.pk).values_list('post', flat=True))
        #自分がいいねした全投稿データを取得
        posts_liked = Post.objects.filter(pk__in=list_of_id_posts_liked).all()
        return posts_liked
           

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        #user_profile.username_slug = user_profile.user.username
        user_profile.profile_picture = "userprofile/default_user.png"
        user_profile.username_slug = slugify(instance.profile.user.username)
        user_profile.display_name = instance.profile.user.username
        user_profile.save()


