from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_user")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster} posted at: {self.timestamp}"
