# Generated by Django 5.1.1 on 2024-10-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0007_rename_author_meetups_organizer"),
    ]

    operations = [
        migrations.AddField(
            model_name="meetups",
            name="is_online",
            field=models.BooleanField(default=False),
        ),
    ]
