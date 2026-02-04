from rest_framework import serializers
from .models import TravelRequest, TravelEntry
from collections import OrderedDict

class TravelEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelEntry
        fields = '__all__'

        extra_kwargs = {
            'travel_request': {'read_only': True}  # <- This is the key fix
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Manually reorder fields
        ordered = OrderedDict()
        for key in [
            'id', 'travel_request', 'travel_Date_from', 'travel_Date_to', 'travel_route_from',
            'travel_route_to', 'fare', 'travel_mode', 'pnr', 'comment', 'billing', 'organization_id', 'created_by', 'is_delete'
        ]:
            ordered[key] = rep.get(key)
        
        return ordered  # ✅ Required

class TravelRequestSerializer(serializers.ModelSerializer):
    entries = TravelEntrySerializer(many=True)

    class Meta:
        model = TravelRequest
        fields = '__all__'

    def create(self, validated_data):
        entries_data = validated_data.pop('entries', [])
        travel_request = TravelRequest.objects.create(**validated_data)
        for entry_data in entries_data:
             TravelEntry.objects.create(travel_request=travel_request, **entry_data)
        return travel_request

    def update(self, instance, validated_data):
        entries_data = validated_data.pop('entries', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # (Optional) delete old and create new entries
        # instance.entries.all().delete()
        # for entry_data in entries_data:
        #     TravelEntry.objects.create(request_id=instance, **entry_data)
        return instance
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Manually reorder fields
        ordered = OrderedDict()
        for key in [
            'id', 'booked_by', 'name', 'booking_date', 'organization_id',
            'created_by', 'is_delete'
        ]:
            ordered[key] = rep.get(key)
        
        # Add 'entries' at the end
        # ordered['entries'] = rep.get('entries')
        
        # Filter out soft-deleted entries
        entries = instance.entries.filter(is_delete=False)
        ordered['entries'] = TravelEntrySerializer(entries, many=True).data
        return ordered
