from rest_framework import serializers
from .models import Entry_Details, Entry_Master, Item_Master, MedalliaData, ReviewPro
from app.models import OrganizationMaster

# from rest_framework import serializers
# from .models import Entry_Details, Entry_Master, OrganizationMaster  # Fix import

class EntryDetailsSerializer(serializers.ModelSerializer):
    Organization_Name = serializers.SerializerMethodField()
    # entry_date = serializers.DateField(source="Entry_Master.EntryDate", read_only=True)
    item_name = serializers.CharField(source="Item_Master.Item", read_only=True)

    class Meta:
        model = Entry_Details
        fields = ["Organization_Name", "item_name", "Value",]

    def get_Organization_Name(self, obj):
        org = OrganizationMaster.objects.filter(OrganizationID=obj.OrganizationID).first()
        return org.ShortDisplayLabel if org else "Unknown Organization"





# Medallia Software Serializer -->
class MedalliaDataSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: ("" if value is None else value) for key, value in data.items()}  # Replace None with ""
    
    class Meta:
        model = MedalliaData
        fields = ["OrganizationID", "EntryDate", "PropertyName", "GuestName", "Month", "CheckInDate", "CheckInProcess", "Cleanliness", "ConditionOfHotel", "WohProgramExperience", "StaffHelpfulness", "RoomNo", "ResponseDate", "CheckOutDate", "WorkingOrder", "CustomerService", "BreakfastExperience", "SpaExperience", "DeliveryHkServices", "NPS", "StaffResponsiveness", "WohAppExperience", "OverallFnbExperience", "PropertyAnticipatedGuestNeeds", "LpMemberSatisfaction", "Comments"]
        

# ReviewPro Software Serializer -->
class ReviewProSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: ("" if value is None else value) for key, value in data.items()}  # Replace None with ""
    
    class Meta:
        model = ReviewPro
        fields = ["OrganizationID", "EntryDate", "Reviewer", "Month", "ReviewRating", "Classification", "Cleanliness", "Location", "LocationScore", "Room", "RoomScore", "GriTM", "PublishedDate", "RatingScale", "Service", "CleanlinessScore", "Value", "ValueScore", "Gastronomy", "GastronomyScore", "Country", "Source", "ReviewScore", "ServiceScore", "DepartmentRatingScale", "ReviewTitle", "ReviewText"]
        