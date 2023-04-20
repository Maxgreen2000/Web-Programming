# Generated by Django 4.1 on 2023-04-19 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wmi', '0003_remove_manuscript_summary_manuscript_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manuscript',
            name='poster',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='manuscipts', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
