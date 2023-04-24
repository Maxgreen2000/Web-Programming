from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# Create your models here.
class Manuscript(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="manuscipts")
    title = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=250, blank=True)
    yearfrom = models.IntegerField(null=True, blank=True)
    yearto = models.IntegerField(null=True, blank=True)
    tags = models.TextField(blank=True)
    transcript = models.TextField(blank=True)
    image = models.ImageField(upload_to='files/manuscriptimages', null=True, blank=True)

    def __str__(self):
        return f"{self.title}, {self.location}, {self.year}"

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.id,
            "title": self.title,
            "location": self.location,
            "yearfrom": self.yearfrom,
            "yearto": self.yearto,
            "tags": self.tags,
            "transcript": self.transcript,
        }