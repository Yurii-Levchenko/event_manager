from django.db import migrations
from django.contrib.auth.models import User

def populate_slugs(apps, schema_editor):
    News = apps.get_model('meetups', 'News')
    Users = apps.get_model('meetups', 'Users')
    
    for news in News.objects.all():
        user = Users.objects.get(pk=news.author_id)
        news.slug = f"{news.title}-{user.full_name}"
        news.save()

class Migration(migrations.Migration):
    dependencies = [
        ('meetups', '0008_meetups_is_online'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]