# Generated by Django 4.1 on 2023-02-01 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wmi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manuscript',
            name='image',
            field=models.ImageField(null=True, upload_to='files/manuscriptimages'),
        ),
    ]
