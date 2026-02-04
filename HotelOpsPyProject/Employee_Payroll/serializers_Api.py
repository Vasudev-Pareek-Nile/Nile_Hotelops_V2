from rest_framework import generics
from .models import Salary_Slip_V1
from .serializers import SalarySlipV1Serializer

# List all salary slips (optionally filter by EmpID, OrganizationID, etc.)
class SalarySlipV1ListAPIView(generics.ListAPIView):
    serializer_class = SalarySlipV1Serializer

    def get_queryset(self):
        queryset = Salary_Slip_V1.objects.filter(IsDelete=False)
        # emp_id = self.request.GET.get('EmpID')
        # org_id = self.request.GET.get('OrganizationID')
        # year = self.request.GET.get('year')
        # month = self.request.GET.get('month')

        # if emp_id:
        #     queryset = queryset.filter(EmpID=emp_id)
        # if org_id:
        #     queryset = queryset.filter(OrganizationID=org_id)
        # if year:
        #     queryset = queryset.filter(year=year)
        # if month:
        #     queryset = queryset.filter(month=month)
        return queryset


# Retrieve single salary slip by ID
class SalarySlipV1DetailAPIView(generics.RetrieveAPIView):
    queryset = Salary_Slip_V1.objects.filter(IsDelete=False)
    serializer_class = SalarySlipV1Serializer
