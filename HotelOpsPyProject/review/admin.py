from django.contrib import admin
from .models import upload_data, FileUpload,OrganizationUrls,PartnerRating



admin.site.register(upload_data)
admin.site.register(OrganizationUrls)
admin.site.register(PartnerRating)

class upload_dataAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'source', 'review_title', 'hotel_rating', 'classification',
        'service_rating', 'clean_rating', 'location', 'value_of_money_rating',
        'room_rating', 'management_response', 'reply_date', 'language'
    )