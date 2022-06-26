from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=400, null=True)

    class Meta:
        verbose_name =('投稿データ')
        verbose_name_plural = ("投稿データ")
        
    def __str__(self):
        return f"{self.pk}"
    
    def post_likes(self):
        """いいね数のカウント"""
        likes = PostLikes.objects.filter(post=self).count()
        return likes
 
    def view_recent_comments(self):
        """投稿に対する最新コメント3つを返す"""
        recent_comments = PostComments.objects.filter(post=self).order_by("-created_at")[:3]
        return recent_comments 

    def post_comments(self):
        comments = PostComments.objects.filter(post=self).count()
        return comments  

        
class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name =('いいね')
        verbose_name_plural = ("いいね")

    def __str__(self):
        return f"{self.user.username}"


class PostComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=140, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name =('コメント')
        verbose_name_plural = ("コメント")
        
    def __str__(self):
        return f"{self.content}"
