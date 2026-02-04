from django.contrib import admin
from .models import Reference_check ,ReferenceDetails,OrganizationNameList,DesignationNameList
# Register your models here.
admin.site.register(Reference_check)

admin.site.register(ReferenceDetails)
admin.site.register(OrganizationNameList)
admin.site.register(DesignationNameList)