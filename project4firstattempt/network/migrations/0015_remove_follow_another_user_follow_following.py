# Generated by Django 4.1 on 2022-10-24 10:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_alter_follow_another_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='another_user',
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
