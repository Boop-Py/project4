from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=255)
    post_time = models.DateTimeField(auto_now=True, null=True ,blank=True)
    liked_by = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_by = models.ManyToManyField(User, blank=True, related_name="followed_by_user")
    following = models.ManyToManyField(User, blank=True, related_name="following_the_user")