from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format = 'JPEG',
        options = {'quality':100},
        null = True,
        blank = True,
    )

    # who is followed by me
    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    # who are the followers
    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    # Am I followed by this user
    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()


class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'my_posts'
    )

    title = models.TextField(blank=True,null=True)

    image = ProcessedImageField(
            upload_to = 'static/images/posts',
            format = 'JPEG',
            options = {'quality':100},
            blank = True,
            null = True,
            )


    def get_absolute_url(self):
        return reverse('post_detail',args=[str(self.id)])

    def get_like_count(self):
        return self.likes.count()


# 链接了 Insta User 和 Post 的关系，用 数据库foreign key 表示
class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = 'likes')
   # related_name 找到哪些人给这个post 点过赞
    user = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'likes'
    )
    # related_name 找到user 给哪些 post 点过赞

    # 一个post和一个 user 的组合是唯一的
    class Meta:
        unique_together = ("post","user")

    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title




