from django.contrib import admin

from .models import ItInformation,SystemDetail,MobileDetail,SimDetail,EmailDetail
List_Display = [ItInformation,SystemDetail,MobileDetail,SimDetail,EmailDetail]
admin.site.register(List_Display)