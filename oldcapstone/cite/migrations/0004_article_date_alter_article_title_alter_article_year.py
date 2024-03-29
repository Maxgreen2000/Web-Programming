# Generated by Django 4.1.4 on 2023-01-13 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cite', '0003_article_title_alter_article_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='year',
            field=models.IntegerField(),
        ),
    ]
