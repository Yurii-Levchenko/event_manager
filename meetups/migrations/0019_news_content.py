# Generated by Django 5.1.1 on 2024-10-18 11:30

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0018_meetups_is_archived_alter_meetups_organizer_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="content",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, null=True
            ),
        ),
    ]
