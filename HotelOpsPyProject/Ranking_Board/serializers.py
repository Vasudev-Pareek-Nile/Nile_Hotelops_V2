from rest_framework import serializers
from .models import Hotel_Ranking

class HotelRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel_Ranking
        fields = '__all__'  # Include all fields
        read_only_fields = ('CreatedDateTime', 'ModifyDateTime')
