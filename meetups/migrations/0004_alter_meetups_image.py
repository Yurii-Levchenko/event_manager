# Generated by Django 5.1.1 on 2024-11-28 10:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0003_tag_meetups_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="meetups",
            name="image",
            field=models.ImageField(
                default="default.jpeg", upload_to="meetups_images/%Y/%m/%d/"
            ),
        ),
    ]
