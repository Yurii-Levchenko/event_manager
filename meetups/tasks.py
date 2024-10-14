from django.db.models import Q
from django.utils import timezone
from django.apps import apps

def archive_meetups():
    Meetups = apps.get_model('meetups', 'Meetups')
    meetups = Meetups.objects.filter(is_archived = False, event_date__lt=timezone.now() + timezone.timedelta(hours=2))
    for meetup in meetups:
        meetup.archive()