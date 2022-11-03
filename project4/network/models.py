from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_user")
    body = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster} posted at: {self.timestamp}"


class Profile(models.Model):
    profile_owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_owner")
    profile_picture = models.ImageField(default='default.jpg')
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.profile_owner.username

class Follow(models.Model):
    user_id = models.ForeignKey(User, null=True, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, null=True, related_name="followers", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user_id.username} has followed {self.following_user_id.username}"
