from django.core.management.base import BaseCommand
from IT_Inventory.utils import send_expiry_reminders, send_expiry_reminders_SecondOne

class Command(BaseCommand):
    help = 'Send email reminders for products expiring soon'

    def handle(self, *args, **kwargs):
        send_expiry_reminders_SecondOne()
        self.stdout.write(self.style.SUCCESS('Reminders sent successfully For 15 days!'))
