# Generated by Django 4.1 on 2022-10-24 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_follow_follower'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='followers',
        ),
    ]
