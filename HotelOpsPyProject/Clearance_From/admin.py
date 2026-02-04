from django.contrib import admin
from .models import MasterClearanceItem,MasterReturnItem,ClearenceEmp,ClearanceItemDetail,ReturnItemDetail
# Register your models here.
admin.site.register(MasterClearanceItem)
admin.site.register(MasterReturnItem)
admin.site.register(ClearenceEmp)
admin.site.register(ClearanceItemDetail)
admin.site.register(ReturnItemDetail)