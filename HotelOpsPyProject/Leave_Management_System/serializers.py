from rest_framework import serializers
from .models import Leave_Type_Master,Leave_Application,Emp_Leave_Balance_Master
from rest_framework.serializers import ModelSerializer

class LeaveTypeMasterSerializer(ModelSerializer):
       class Meta:
            model = Leave_Type_Master
            fields = ['id','Type']    

class EmpLeaveBalanceSerializer(ModelSerializer):
   
    Leave_Type_Master_ID = serializers.PrimaryKeyRelatedField(source='Leave_Type_Master.id', read_only=True)
    Leave_Type_Master_Type = serializers.CharField(source='Leave_Type_Master.Type', read_only=True)
    
    class Meta:
        model = Emp_Leave_Balance_Master
        fields = ['id', 'Emp_code', 'Leave_Type_Master_ID', 'Leave_Type_Master_Type', 'Balance']




class LeaveApplicationSerializer(ModelSerializer):
    Leave_Type_Master_ID = serializers.PrimaryKeyRelatedField(source='Leave_Type_Master.id', read_only=True)
    Leave_Type_Master_Type = serializers.CharField(source='Leave_Type_Master.Type', read_only=True)

    class Meta:
        model = Leave_Application
        fields = ['id', 'Leave_Type_Master_Type','Leave_Type_Master_ID', 'Emp_code', 'Start_Date', 'End_Date', 'Reason', 'Status', 'From_1st_Half','From_2nd_Half','To_1st_Half' ,'To_2nd_Half','Total_credit', 'ReportingtoDesigantion', 'OrganizationID', 'CreatedBy', 'CreatedDateTime', 'ModifyBy', 'ModifyDateTime', 'IsDelete']



