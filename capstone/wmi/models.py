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
    imageurl = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title}, {self.location}, {self.yearfrom} - {self.yearto}"

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
            "imageurl": self.imageurl
        }
    
class Email(models.Model):
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
    recipient = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_received", null=True)
    manuscript = models.ForeignKey("Manuscript", on_delete=models.PROTECT, related_name="manuscriptid")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"email ID: {self.id} from {self.sender} sent to {self.recipient} at {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "recipient": [self.recipient.username],
            "manuscripttitle": self.manuscript.title,
            "manuscriptid": self.manuscript.id,
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "archived": self.archived
        }

class Conversation(models.Model):
    manuscript = models.ForeignKey("Manuscript", on_delete=models.PROTECT, related_name="conversation_manuscriptid")
    participants = models.ManyToManyField("User", related_name="conversation_participants")
    emails = models.ManyToManyField("Email", related_name="conversation_emails")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"manuscript: {self.manuscript.title} conversation between {self.participants.all()}"

    def serialize(self):
        return {
            "id": self.id,
            "manuscript": self.manuscript.title,
            "manuscript_id": self.manuscript.id,
            "participants": [user.username for user in self.participants.all()],
            "participants_id": [user.id for user in self.participants.all()],
            "emails_id": [email.id for email in self.emails.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }