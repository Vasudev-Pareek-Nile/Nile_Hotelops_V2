from django.urls import path
from .views import *

urlpatterns = [
    path('',salary_structure,name='salary_structure'),
    path('salary_Calc',salary_Calc,name='salary_Calc'),
    # path('Salary_Calc_Ready', Salary_Calc_Ready,name='Salary_Calc_Ready'),
    path('Salary_Calc_Ready/<str:Orgid>/', Salary_Calc_Ready,name='Salary_Calc_Ready'),

    path('Handle_SalaryStructure', Handle_SalaryStructure,name='Handle_SalaryStructure'),

    path('Handle_PT_Configration', Handle_PT_Configration,name='Handle_PT_Configration'),
    # path('salary_Calc_post_value', salary_Calc_post_value,name='salary_Calc_post_value'),

    # path('Salary_Calc_Ready_api', Salary_Calc_Ready_api,name='Salary_Calc_Ready_api'),

    path('Delete_Salary_Structure/<int:id>/', Delete_Salary_Structure,name='Delete_Salary_Structure'),

    path('api/OrganizationList/', OrganizationList,name='OrganizationList'),
    path('api/organization-list/<int:user_orgid>/<str:session_Orgid>/', OrganizationList,name='OrganizationList'),


    # path("api/salary-structure/", SalaryStructureAPI, name="SalaryStructureAPI"),
    path("api/salary-structure/<str:Orgid>/", SalaryStructureAPI, name="SalaryStructureAPI"),
]
