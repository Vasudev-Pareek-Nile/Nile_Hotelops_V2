from django.contrib import admin
from .models import HREmployeeChecklistMaster,HREmployeeChecklist_Entry,HREmployeeChecklist_Details
# Register your models here.
admin.site.register(HREmployeeChecklistMaster)
admin.site.register(HREmployeeChecklist_Entry)
admin.site.register(HREmployeeChecklist_Details)