from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(blank=True, max_length=255)
    day = models.CharField(blank=True, max_length=255)
    month = models.CharField(blank=True, max_length=255)
    year = models.CharField(max_length=255)
    journal = models.CharField(blank=True, max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.title}, {self.author}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "journal": self.journal,
            "content": self.content,
        }
