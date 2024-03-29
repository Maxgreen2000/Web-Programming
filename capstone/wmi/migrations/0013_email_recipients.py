# Generated by Django 4.1 on 2023-04-25 12:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wmi', '0012_remove_email_recipients'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='recipients',
            field=models.ManyToManyField(related_name='emails_received', to=settings.AUTH_USER_MODEL),
        ),
    ]
