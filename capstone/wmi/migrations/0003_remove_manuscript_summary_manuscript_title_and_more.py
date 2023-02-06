# Generated by Django 4.1 on 2023-02-02 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wmi', '0002_manuscript_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manuscript',
            name='summary',
        ),
        migrations.AddField(
            model_name='manuscript',
            name='title',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='files/manuscriptimages'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='location',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='tags',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='transcript',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]