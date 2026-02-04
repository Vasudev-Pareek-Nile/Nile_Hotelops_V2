from datetime import date

from django.core.management.base import BaseCommand
from EmailReader.views import download_email_data

class Command(BaseCommand):
    def handle(self, *args, **options):
       
        download_email_data()

        self.stdout.write(self.style.SUCCESS(f'Data transferred successfully for  records'))
