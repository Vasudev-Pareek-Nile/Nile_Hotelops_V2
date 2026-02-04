from rest_framework import serializers
from .models import Assessment_Master

class AssessmentMasterMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_Master
        fields = '__all__'
        # fields = [
        #     'id',
        #     'Name',
        #     'Email',
        #     'Department',
        #     'Level',
        #     'InterviewDate',
        #     'Status',
        #     'LastApporvalStatus',
        # ]