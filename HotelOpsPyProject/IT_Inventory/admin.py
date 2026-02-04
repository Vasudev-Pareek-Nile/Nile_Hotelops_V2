from django.contrib import admin
from .models import IT_Inventory,Master_Category,Master_Company,Master_Area,Master_Software_type
# Register your models here.
admin.site.register(IT_Inventory)
admin.site.register(Master_Category)
admin.site.register(Master_Company)
admin.site.register(Master_Area)
admin.site.register(Master_Software_type)
