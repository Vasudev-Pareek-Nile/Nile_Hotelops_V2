from django.core.management.base import BaseCommand
# from services.send_padp_notification import run_padp_notification
from PADP.services.send_padp_notification import run_padp_notification

class Command(BaseCommand):
    help = "Send PADP pending approval notifications"

    def add_arguments(self, parser):
        parser.add_argument("--user_id", default="20201212180048")
        parser.add_argument("--org_id", default="3")
        parser.add_argument("--user_type", default="hod")
        parser.add_argument("--month", default="All")
        parser.add_argument("--Designation", default=None)
        parser.add_argument("--I", default="333333")

    def handle(self, *args, **options):
        result = run_padp_notification(
            UserID=options["user_id"],
            OrganizationID=options["org_id"],
            UserType=options["user_type"],
            month=options["month"],
            Designation=options["Designation"],
            I=options["I"],
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ PADP Notification Sent | Count: {result['count']}"
            )
        )
