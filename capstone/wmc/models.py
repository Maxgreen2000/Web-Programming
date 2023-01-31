from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# Create your models here.
class Manuscript(models.Model):
    summary = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    tags = models.TextField()
    transcript = models.TextField()

    def __str__(self):
        return f"{self.summary}, {self.location}, {self.year}"

    def serialize(self):
        return {
            "id": self.id,
            "summary": self.summary,
            "location": self.location,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "tags": self.tags,
            "transcript": self.transcript,
        }