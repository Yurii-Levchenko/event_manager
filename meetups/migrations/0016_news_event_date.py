# Generated by Django 5.1.1 on 2024-10-07 11:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0015_news_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="event_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
