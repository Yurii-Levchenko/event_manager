# Generated by Django 5.1.1 on 2024-10-05 13:37

import location_field.models.plain
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0012_alter_news_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="meetups",
            name="location",
            field=location_field.models.plain.PlainLocationField(
                blank=True, default="49,24", max_length=63
            ),
        ),
    ]
