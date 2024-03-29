# Generated by Django 4.1 on 2023-05-17 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wmi', '0016_conversation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='emails',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='participants',
        ),
        migrations.AddField(
            model_name='conversation',
            name='emails',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='conversation_emails', to='wmi.email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conversation',
            name='participants',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='conversation_participants', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
