# Generated by Django 4.1 on 2022-10-12 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_listing_price_listing_highestbid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bidCounter',
            field=models.IntegerField(default=0),
        ),
    ]