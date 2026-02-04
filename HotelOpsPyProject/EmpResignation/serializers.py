
from rest_framework import serializers
from .models import EmpResigantionModel


class Employee_Resignation_F_And_F_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmpResigantionModel
        fields = [
            "IsDEPT",
            "HK",
            "IT",
            "HR",
        ]

