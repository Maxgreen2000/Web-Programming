from email.policy import default
from tokenize import blank_re
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, null=True)



class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_user")
    body = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster} posted at: {self.timestamp}"


class Profile(models.Model):
    profile_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_owner")
    profile_picture = models.ImageField(default='default.jpg')
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.profile_owner.username






