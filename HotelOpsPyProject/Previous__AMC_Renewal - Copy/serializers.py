from rest_framework import serializers
from .models import AMC_Entry_Master


class AMCEntryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AMC_Entry_Master
        fields = "__all__"
