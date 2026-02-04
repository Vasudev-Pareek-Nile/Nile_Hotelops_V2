from django.contrib import admin
from .models import Product_Master,Product_Group_Master,Product_Group_Mapping

admin.site.register(Product_Master)
admin.site.register(Product_Group_Master)
admin.site.register(Product_Group_Mapping)


# Register your models here.
