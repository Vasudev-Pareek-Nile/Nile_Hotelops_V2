from django.contrib import admin

# Register your models here.
from .models import Task,HotelOpDetails,projectss,user
# Register your models here.
admin.site.register(Task)
admin.site.register(HotelOpDetails)
admin.site.register(projectss)
admin.site.register(user)