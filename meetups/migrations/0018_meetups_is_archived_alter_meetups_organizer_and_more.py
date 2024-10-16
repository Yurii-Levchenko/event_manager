# Generated by Django 5.1.1 on 2024-10-14 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0017_remove_news_event_date_meetups_event_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="meetups",
            name="is_archived",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="meetups",
            name="organizer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="meetups.users",
            ),
        ),
        migrations.AlterField(
            model_name="news",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="meetups.users",
            ),
        ),
    ]
