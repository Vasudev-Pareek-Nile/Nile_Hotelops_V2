from rest_framework import serializers
from .models import UserSession

class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = [
            'user_id', 'auth_token', 'session_key', 'organization_name', 'domain_code',
            'organization_logo', 'full_name', 'employee_code', 'level', 'department_name',
            'user_type', 'organization_id', 'emp_id', 'division_name', 'Designation'
        ]
