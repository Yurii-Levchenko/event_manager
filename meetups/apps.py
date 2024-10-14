from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import archive_meetups

class MeetupsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "meetups"

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(archive_meetups, 'interval', minutes = 30)
        scheduler.start()

