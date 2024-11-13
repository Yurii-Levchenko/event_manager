# Generated by Django 5.1.1 on 2024-10-02 11:53

import location_field.models.plain
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Meetup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField()),
                ("country", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=200)),
                (
                    "location",
                    location_field.models.plain.PlainLocationField(
                        default="0,0", max_length=63
                    ),
                ),
            ],
        ),
    ]