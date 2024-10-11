# Generated by Django 5.1.1 on 2024-10-07 12:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0016_news_event_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="news",
            name="event_date",
        ),
        migrations.AddField(
            model_name="meetups",
            name="event_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
