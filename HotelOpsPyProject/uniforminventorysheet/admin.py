from django.contrib import admin
from .models import Uniform_Inventory_Sheet,Uniform_Item_Master,Uniform_Item_detail

# Register your models here.
admin.site.register(Uniform_Inventory_Sheet)
admin.site.register(Uniform_Item_Master)
admin.site.register(Uniform_Item_detail)