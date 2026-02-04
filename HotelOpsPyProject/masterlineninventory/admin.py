from django.contrib import admin
from .models import Linen_Inventory_Sheet,Linen_Item_Master,Linen_Item_Details

# Register your models here.
admin.site.register(Linen_Inventory_Sheet)
admin.site.register(Linen_Item_Master)
admin.site.register(Linen_Item_Details)
