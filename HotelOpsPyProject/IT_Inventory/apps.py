from django.apps import AppConfig


class ItInventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IT_Inventory'



from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from django.core.management import call_command

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IT_Inventory'

    def ready(self):
        from .utils import send_expiry_reminders
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_expiry_reminders, 'cron', hour=17, minute=7)
        scheduler.start()
