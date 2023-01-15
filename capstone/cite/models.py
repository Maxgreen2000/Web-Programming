from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(blank=True, max_length=255)
    year = models.IntegerField(null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.title}, {self.author}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "year": self.year,
            "content": self.content,
        }

class Project(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="projects")
    articles = models.ManyToManyField("Article", related_name="emails_received")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.sender.username,
            "articles": [article.id for article in self.articles.all()],
        }