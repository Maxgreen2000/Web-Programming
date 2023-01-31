from django.contrib import admin
from .models import User, Article, Project, Citation

# Register your models here.
admin.site.register(User)
admin.site.register(Article)
admin.site.register(Project)
admin.site.register(Citation)