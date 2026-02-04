from app.models import OrganizationMaster
from django.core.management.base import BaseCommand
from ...parsing import social_data
class Command(BaseCommand):
    help = 'Description of your command'
    def handle(self, *args, **options):
        source_list=['Booking','MakeMyTrip','Agoda']
        social_data(source_list)