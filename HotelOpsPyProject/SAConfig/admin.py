from django.contrib import admin
from .models import ProductGroup,Product

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductGroup)