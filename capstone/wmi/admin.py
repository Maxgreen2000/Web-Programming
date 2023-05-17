from django.contrib import admin
from .models import User, Manuscript, Email, Conversation

# Register your models here.
admin.site.register(User)
admin.site.register(Manuscript)
admin.site.register(Email)
admin.site.register(Conversation)

