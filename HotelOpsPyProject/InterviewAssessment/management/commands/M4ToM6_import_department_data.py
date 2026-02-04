

import pandas as pd
from django.core.management.base import BaseCommand
from InterviewAssessment.models import DepartmentLevelConfig, DepartmentLevelConfigDetails

class Command(BaseCommand):
    help = "Import department data from Excel"

    def handle(self, *args, **kwargs):
        file_path = "C:/Users/admin/Downloads/M4ToM6Config.xlsx"

        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            department_config = DepartmentLevelConfig.objects.create(
                Department=row["Department"],
                HeadDepartment=row["HeadDepartment"],
                Level=row["Levels"],
             OrganizationID =  3 
            )

            level_sort_order = ["Level 1", "Level 2"]
            for sort_order in level_sort_order:
                DepartmentLevelConfigDetails.objects.create(
                    DepartmentLevelConfig=department_config,
                    LevelSortOrder=sort_order,
                    UserType=row[sort_order],
                     OrganizationID =  3 
                )

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
