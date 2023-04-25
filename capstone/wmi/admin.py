from django.contrib import admin
from .models import User, Manuscript, Email

# Register your models here.
admin.site.register(User)
admin.site.register(Manuscript)
admin.site.register(Email)

