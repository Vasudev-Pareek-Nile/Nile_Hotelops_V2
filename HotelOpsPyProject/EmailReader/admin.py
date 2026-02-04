from django.contrib import admin

# Register your models here.
from .models import Resume,Designation
admin.site.register(Designation)
admin.site.register(Resume)