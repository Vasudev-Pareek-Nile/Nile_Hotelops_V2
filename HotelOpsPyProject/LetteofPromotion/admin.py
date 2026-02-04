from django.contrib import admin
from .models import PromotionLetterEmployeeDetail,PromotionLetterDeletedFileofEmployee,PromotionLetter
# Register your models here.
admin.site.register(PromotionLetterEmployeeDetail)
admin.site.register(PromotionLetter)
admin.site.register(PromotionLetterDeletedFileofEmployee)
