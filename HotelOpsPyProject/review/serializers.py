from rest_framework import serializers
from .models import upload_data

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = upload_data
        fields = '__all__'