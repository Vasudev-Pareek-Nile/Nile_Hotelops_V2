from datetime import date

from django.core.management.base import BaseCommand
from EmailReader.views import upload_EmailData

class Command(BaseCommand):
    def handle(self, *args, **options):
       
        upload_EmailData()

        self.stdout.write(self.style.SUCCESS(f'Data transferred successfully for  records'))
