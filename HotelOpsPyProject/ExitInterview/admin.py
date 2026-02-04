from django.contrib import admin
from .models import Rating,Experience,Reason_for_Leaving,Exitinterviewdata,exitinterviewmaster,ExitRating

# Register your models here.
admin.site.register(Rating)
admin.site.register(Experience)
admin.site.register(Reason_for_Leaving)
admin.site.register(Exitinterviewdata)
admin.site.register(exitinterviewmaster)
admin.site.register(ExitRating)