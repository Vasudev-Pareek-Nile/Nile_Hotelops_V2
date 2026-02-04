from django.contrib import admin
from .models import VerbalWarningmoduls,WrittenWarningModul,FinalWarningModule,WarningMasterDetail
# Register your models here.
admin.site.register(VerbalWarningmoduls)
admin.site.register(WrittenWarningModul)
admin.site.register(FinalWarningModule)
admin.site.register(WarningMasterDetail)