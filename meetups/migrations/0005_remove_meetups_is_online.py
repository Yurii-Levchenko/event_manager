# Generated by Django 5.1.1 on 2024-10-04 14:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0004_alter_meetups_options_alter_news_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="meetups",
            name="is_online",
        ),
    ]
