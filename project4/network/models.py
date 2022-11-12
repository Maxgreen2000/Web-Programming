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

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "body": self.body,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }


class Profile(models.Model):
    profile_owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_owner")
    profile_picture = models.ImageField(default='default.jpg')
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.profile_owner.username

    def serialize(self):
        return {
            "id": self.id,
            "profile_owner": self.profile_owner.username,
            "bio": self.bio
        }

class Follow(models.Model):
    user_id = models.ForeignKey(User, null=True, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, null=True, related_name="followers", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user_id.username} has followed {self.following_user_id.username}"

class Like(models.Model):
    liker = models.ForeignKey(User, null=True, related_name="likeuser", on_delete=models.CASCADE)
    liked_Post = models.ForeignKey(Post, null=True, related_name="likepost", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.liker.username} has liked post id: {self.liked_Post.id}"