from rest_framework import serializers
from .models import OnRollDesignationMaster

class OnRollDesignationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnRollDesignationMaster
        fields = '__all__'
