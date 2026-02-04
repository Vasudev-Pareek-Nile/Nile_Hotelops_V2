from rest_framework import serializers
from .models import Full_and_Final_Settltment
from EmpResignation.serializers import Employee_Resignation_F_And_F_Serializer
from EmpResignation.models import EmpResigantionModel


class FullAndFinalSettlementSerializer(serializers.ModelSerializer):
    Tenure = serializers.SerializerMethodField()
    Clearance = serializers.SerializerMethodField()

    class Meta:
        model = Full_and_Final_Settltment
        fields = [
            "id",
            "Name",
            "Emp_Code",
            "DOJ",
            "Date_Of_Leaving",
            "Dept",
            "Designation",
            "EmpStatus",
            "FinalStatus",
            "AuditedByHR",
            "AuditedByFinance",
            "AuditedByGM",
            "AuditedBy_Auditor",
            "Tenure",
            "OrganizationID",
            "Clearance"
        ]

    def get_Tenure(self, obj):
        if not obj.DOJ or not obj.Date_Of_Leaving:
            return None
        
        delta = obj.Date_Of_Leaving - obj.DOJ
        
        # Convert days to years/months/days
        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30

        return {
            "years": years,
            "months": months,
            "days": days,
            "total_days": delta.days
        }
        
        
    def get_Clearance(self, obj):
        resignation = EmpResigantionModel.objects.filter(
            Emp_Code=obj.Emp_Code,
            IsDelete=False
        ).first()

        if resignation:
            return Employee_Resignation_F_And_F_Serializer(resignation).data
        return None

