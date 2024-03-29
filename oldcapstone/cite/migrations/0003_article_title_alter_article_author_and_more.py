# Generated by Django 4.1.4 on 2023-01-08 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cite', '0002_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='day',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='journal',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='month',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='publisher',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='year',
            field=models.CharField(max_length=255),
        ),
    ]
