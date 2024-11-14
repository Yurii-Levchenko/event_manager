# Generated by Django 5.1.1 on 2024-11-14 14:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0002_meetups_news_delete_meetup"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("caption", models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name="meetups",
            name="tags",
            field=models.ManyToManyField(blank=True, to="meetups.tag"),
        ),
    ]
