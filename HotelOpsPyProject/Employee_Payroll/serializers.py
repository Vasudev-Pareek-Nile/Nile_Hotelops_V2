from rest_framework import serializers
from .models import Salary_Slip_V1

class AlifFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SalarySlipV1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Salary_Slip_V1
        fields = '__all__'
        

class Excel_Attendance_Upload_Serializer(serializers.Serializer):
    file = serializers.FileField()

