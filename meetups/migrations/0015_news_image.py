# Generated by Django 5.1.1 on 2024-10-07 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0014_meetups_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="news_images/%Y/%m/%d/"
            ),
        ),
    ]
