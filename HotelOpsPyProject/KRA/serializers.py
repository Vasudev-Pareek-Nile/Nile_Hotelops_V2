from rest_framework import serializers
from .models import KRA,HotelKRAStandard

class KRASerializer(serializers.ModelSerializer):
    class Meta:
        model = KRA
        fields = '__all__'

class HotelKRAStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelKRAStandard
        fields = '__all__'