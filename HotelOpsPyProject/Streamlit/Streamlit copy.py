import os
import sys
import django

from datetime import date
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pandas as pd
from django.db.models import OuterRef, Subquery,Func,F


#import redis
import streamlit as st
import pickle

class DatePartYear(Func):
    function = 'DATEPART'
    template = '%(function)s(YEAR, %(expressions)s)'


#redis_client = redis.StrictRedis(PyHost="127.0.0.1", port=6379, db=1)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelopsmgmtpy.settings')
django.setup()




from app.models import OrganizationMaster

from ExitInterview.models import Exitinterviewdata
from FullandFinalSettlement.models import Full_and_Final_Settltment
from Leave_Management_System.models import Emp_Leave_Balance_Master
from EmpAbsconding.models import EmpAbscondingModel
from EmpTermination.models import EmpTerminationModel
from EmpResignation.models import EmpResigantionModel
from HumanResources.models import EmployeePersonalDetails,EmployeeWorkDetails,EmployeeEmergencyInformationDetails
from InterviewAssessment.models import Assessment_Master
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.db.models import OuterRef, Subquery

from Manning_Guide.models import OnRollDesignationMaster,OnRollDepartmentMaster,LavelAdd, OnRollDivisionMaster  




import datetime
from datetime import datetime
import pandas as pd

from app.models import ReportModuleMaster



import requests
import streamlit as st

import streamlit as st
favicon_path = "./favicon.ico" 
st.set_page_config(page_title="HotelOps Report", page_icon=favicon_path)
import streamlit as st
import time
import streamlit as st


def custom_loading():
    # Create a placeholder for the loading message
    placeholder = st.empty()

    # Display a custom loading message
    with placeholder.container():
        st.markdown(
            """
            <div style="text-align: center; font-size: 20px; font-weight: bold; color: #007BFF;">
                🔄 Please wait... Processing your request
            </div>
            """,
            unsafe_allow_html=True
        )
    
    
    time.sleep(5) 

    
    placeholder.empty()

   
custom_loading()

query_params = st.query_params
user_id = query_params.get("token", [None])

if user_id == [None]:
    # print("----------------------")
    error_page_html = """
    <div style="text-align: center; padding: 50px; background-color: #1C294B; border: 1px solid #f5c6cb; border-radius: 10px;">
        <h2 style="color: #FFFFFF">HotelOps</h2>
        <img src="https://hotelopsblob.blob.core.windows.net/hotelopslogos/HotelOpsLogo.png" alt="Access Denied" style="width: 300px; height: 200px; margin-bottom: 20px;">
        <p style="color: #FFFFFF; font-size: 18px;">Please login to continue</p>
        <a href="http://127.0.0.1:8000/" style="text-decoration: none;">
            <button style="padding: 12px 20px; background-color: #007bff; color: white; border-radius: 5px; font-size: 16px; cursor: pointer;">
                Click here to login
            </button>
        </a>
    </div>
    """
    
    
    st.markdown(error_page_html, unsafe_allow_html=True)
    
    st.stop()
else:
    if user_id:
        API_URL = f"https://hotelops.in:8080/api/user-session/{user_id}/"
        
        auth_token = "YOUR_AUTH_TOKEN_HERE"  
        
        headers = {
            "Authorization": f"Bearer {auth_token}"  
        }

        response = requests.get(API_URL, headers=headers)
        

        if response.status_code == 200:
            data = response.json()

            full_name = data.get('full_name', 'N/A')
            department_name = data.get('department_name', 'N/A')
            organization_name = data.get('organization_name', '')

            card_css = """
            <style>
                /* Style the sidebar background color */
                .css-1d391kg {
                    background-color: #1E3A8A;  /* Blue color for sidebar */
                }
            [class*="st-key"] {
                margin-left:10px !important;
            }

                /* Card styling */
                .card .name, .card .department {
                    border-radius: 5px;
                    font-size: 15px;
                    margin-bottom: 5px;
                }
            </style>
            """

            with st.sidebar:
                st.markdown(card_css, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="card" style="text-align: center;">
                    <div class="name">{organization_name}</div>
                    <div class="name">{full_name}, {department_name}</div>  
                </div>
                """, unsafe_allow_html=True)

            if 'organization_id' in data:
                st.session_state.organization_id = data['organization_id']
            else:
                st.write("No Organization ID found in the user session data.")
            
            OID = str(st.session_state.organization_id)

            # Fetch organizations based on the selected organization ID
            if OID == '3':
                memOrg = OrganizationMaster.objects.filter(IsDelete=False, Activation_status='1').values('OrganizationID', 'OrganizationName')
                organization_list = [org['OrganizationName'] for org in memOrg]
                organization_ids = [str(org['OrganizationID']) for org in memOrg]

                organization_list.insert(0, 'All')  
                organization_ids.insert(0, 'All')   
            else:
                memOrg = OrganizationMaster.objects.filter(OrganizationID=OID, IsDelete=False, Activation_status='1').values('OrganizationID', 'OrganizationName')

                organization_list = [org['OrganizationName'] for org in memOrg]
                organization_ids = [str(org['OrganizationID']) for org in memOrg]

            

            selected_org = st.sidebar.selectbox(
                "Choose an organization", 
                organization_list, 
                index=organization_ids.index(str(st.session_state.organization_id)) if str(st.session_state.organization_id) in organization_ids else 0
            )

            selected_org_id = organization_ids[organization_list.index(selected_org)]

            # If "All" is selected, remove the session's organization_id
            if selected_org_id == 'All':
                org_id = None
                if 'organization_id' in st.session_state:
                    del st.session_state.organization_id  # Clear session organization ID
            else:
                org_id = selected_org_id

            # Display data based on organization selection
            if org_id is None:
                all_org_data = OrganizationMaster.objects.filter(IsDelete=False, Activation_status='1').values('OrganizationID', 'OrganizationName')
                
            else:
                specific_org_data = OrganizationMaster.objects.filter(OrganizationID=org_id).values('OrganizationID', 'OrganizationName')
                
        else:
            st.write()
    else:
        st.write("No User ID found.")

if 'organization_id' not in st.session_state:
    st.session_state.organization_id = None
    error_page_html = """
    <div style="text-align: center; padding: 50px; background-color: #1C294B; border: 1px solid #f5c6cb; border-radius: 10px;">
        <h2 style="color: #FFFFFF">HotelOps</h2>
        <img src="https://hotelopsblob.blob.core.windows.net/hotelopslogos/HotelOpsLogo.png" alt="Access Denied" style="width: 300px; height: 200px; margin-bottom: 20px;">
        <p style="color: #FFFFFF; font-size: 18px;">Please login to continue</p>
        <a href="http://127.0.0.1:8000/" style="text-decoration: none;">
            <button style="padding: 12px 20px; background-color: #007bff; color: white; border-radius: 5px; font-size: 16px; cursor: pointer;">
                Click here to login
            </button>
        </a>
    </div>
    """
    
    # Display the error page with the HTML template
    st.markdown(error_page_html, unsafe_allow_html=True)
    
    st.stop() 




from Manning_Guide.models import ServicesDepartmentMaster,ServicesDesignationMaster,ContractDesignationMaster,ContractDepartmentMaster


module_names = ReportModuleMaster.objects.filter(IsDelete=False).values_list('Module_Name', flat=True).distinct()
module_names = list(module_names)  # Convert to list

# Default to "Human Resources" if present, else default to the first module
selected_module = st.sidebar.selectbox(
    "Choose a Module", 
    module_names, 
    index=module_names.index('Human Resources') if 'Human Resources' in module_names else 0
)

# Filter report options based on the selected module
report_options = ReportModuleMaster.objects.filter(
    Module_Name=selected_module, IsDelete=False
).values_list('Report_title', flat=True).distinct()

report_options = list(report_options)  # Convert to list


selected_report = st.sidebar.selectbox(
    "Choose a report type", 
    report_options, 
    index=report_options.index('Master Report') if 'Master Report' in report_options else 0
)


print("selected report is here:::---", selected_report)




if selected_report == "Actual Shared Services":
   
    departments = ServicesDepartmentMaster.objects.filter(
        IsDelete=False
    ).values_list('DepartmentName', flat=True).distinct()

    selected_department = st.sidebar.selectbox("Choose a Department", ['All'] + list(departments))

   
    if selected_department != 'All':
        filtered_designations = ServicesDesignationMaster.objects.filter(
            ServicesDepartmentMaster__DepartmentName=selected_department,
            IsDelete=False
        ).values_list('designations', flat=True).distinct()
    else:
        filtered_designations = ServicesDesignationMaster.objects.filter(
            IsDelete=False
        ).values_list('designations', flat=True).distinct()

    selected_designation = st.sidebar.selectbox("Choose a Designation", ['All'] + list(filtered_designations))


elif selected_report == "Budget Shared Services Report":
    
    departments = ServicesDepartmentMaster.objects.filter(
        IsDelete=False
    ).values_list('DepartmentName', flat=True).distinct()

    selected_department = st.sidebar.selectbox("Choose a Department", ['All'] + list(departments))

    
    if selected_department != 'All':
        filtered_designations = ServicesDesignationMaster.objects.filter(
            ServicesDepartmentMaster__DepartmentName=selected_department,
            IsDelete=False
        ).values_list('designations', flat=True).distinct()
    else:
        filtered_designations = ServicesDesignationMaster.objects.filter(
            IsDelete=False
        ).values_list('designations', flat=True).distinct()

    selected_designation = st.sidebar.selectbox("Choose a Designation", ['All'] + list(filtered_designations))

elif selected_report == "Actual Contract Report":
    
    departments = ContractDepartmentMaster.objects.filter(
        IsDelete=False
    ).values_list('DepartmentName', flat=True).distinct()

    selected_department = st.sidebar.selectbox("Choose a Department", ['All'] + list(departments))

    
    if selected_department != 'All':
        filtered_designations = ContractDesignationMaster.objects.filter(
            ContractDepartmentMaster__DepartmentName=selected_department,
            IsDelete=False
        ).values_list('designations', flat=True).distinct()
    else:
        filtered_designations = ContractDesignationMaster.objects.filter(
            IsDelete=False
        ).values_list('designations', flat=True).distinct()

    selected_designation = st.sidebar.selectbox("Choose a Designation", ['All'] + list(filtered_designations))

elif selected_report == "Budget Contract Report":
    
    departments = ContractDepartmentMaster.objects.filter(
        IsDelete=False
    ).values_list('DepartmentName', flat=True).distinct()

    selected_department = st.sidebar.selectbox("Choose a Department", ['All'] + list(departments))

    
    if selected_department != 'All':
        filtered_designations = ContractDesignationMaster.objects.filter(
            ContractDepartmentMaster__DepartmentName=selected_department,
            IsDelete=False
        ).values_list('designations', flat=True).distinct()
    else:
        filtered_designations = ContractDesignationMaster.objects.filter(
            IsDelete=False
        ).values_list('designations', flat=True).distinct()

    selected_designation = st.sidebar.selectbox("Choose a Designation", ['All'] + list(filtered_designations))    

else:
    
    Division = OnRollDivisionMaster.objects.filter(
        IsDelete=False
    ).values_list('DivisionName', flat=True).distinct()
    
    selected_Division = st.sidebar.selectbox("Choose a Division", ['All'] + list(Division))
    # print("selected division is here:::---", selected_Division)
    # selected_Division = st.sidebar.selectbox("Choose a Division", ['All'] + list(Division))
    # selected_division = st.sidebar.selectbox("Choose a Division", ['All'] + list(divisions))

# OnRollDepartmentMaster>OnRollDivisionMaster(foreign key) > DivisionName
    # if selected_Division != 'All':
    #     filtered_departments = OnRollDepartmentMaster.objects.filter(
    #         OnRollDivisionMaster__DivisionName=selected_Division,
    #         IsDelete=False
    #     ).values_list('DepartmentName', flat=True).distinct()
    # else:
    #     filtered_departments = OnRollDivisionMaster.objects.filter(
    #         IsDelete=False
    #     ).values_list('DepartmentName', flat=True).distinct()


    if selected_Division == 'All':
        filtered_departments = OnRollDepartmentMaster.objects.filter(
            IsDelete=False
        ).values_list('DepartmentName', flat=True).distinct()
    else:
        filtered_departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_Division,
            IsDelete=False
        ).values_list('DepartmentName', flat=True).distinct()


    # departments = OnRollDepartmentMaster.objects.filter(
    #     IsDelete=False
    # ).values_list('DepartmentName', flat=True).distinct()

    selected_department = st.sidebar.selectbox("Choose a Department", ['All'] + list(filtered_departments))

   
    if selected_department != 'All':
        filtered_designations = OnRollDesignationMaster.objects.filter(
            OnRollDepartmentMaster__DepartmentName=selected_department,
            IsDelete=False
        ).values_list('designations', flat=True).distinct()
    else:
        filtered_designations = OnRollDesignationMaster.objects.filter(
            IsDelete=False
        ).values_list('designations', flat=True).distinct()

    selected_designation = st.sidebar.selectbox("Choose a Designation", ['All'] + list(filtered_designations))




levels = LavelAdd.objects.filter(IsDelete=False).values_list('lavelname', flat=True).distinct()


levels = list(levels)  
levels.insert(0, 'All')  


selected_level = st.sidebar.selectbox("Choose a level", levels)






current_year = date.today().year
# Define a static list of years
# years = ["2020", "2021", "2022", "2023", "2024", "2025"]  # Modify this list as needed
years = [str(year) for year in range(current_year, 2017, -1)]


# years.insert(0, "Select a year")  


selected_year = st.sidebar.multiselect("Choose a year", years)


if not selected_year:
    selected_year = years




months = ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December']


selected_months = st.sidebar.multiselect("Choose months", months, default=None)


if not selected_months:
    selected_months = months



# report_options = ["Employees on Resignation", "Employees on Termination", "New Joinees Report",'Emergency Contact Report',"Blood Group Report",'Absconding Employees Report',"Upcoming Birthday's report","Employees on Probation",'Employees Serving Notice Period','Exit Interview Report','Leave balance report','Pending appointment letters','Pending Confirmation Letters','Full and final pending with auditors report','Full and final pending with finance report','Pending full and final report','Full and final pending clearance report','Department wise manning report','Attrition Report']
# selected_report = st.sidebar.selectbox("Choose a report type", report_options)



# Fetch module names and add "All" as the default option







from django.core.exceptions import ObjectDoesNotExist

def get_organization_short_name(org_id):
    try:
        # If org_id is None or blank, return all organizations' short names
        if not org_id:
            organizations = OrganizationMaster.objects.all()  # Fetch all organizations
            return [organization.ShortDisplayLabel for organization in organizations]
        
        # Fetch organization by ID if org_id is provided
        organization = OrganizationMaster.objects.get(OrganizationID=org_id)
        return organization.ShortDisplayLabel
    except ObjectDoesNotExist:
        return f"Organization with ID {org_id} not found."




def fetch_filtered_data(report_type, report_options, org_id, selected_Division, selected_department, selected_designation, selected_year, selected_months, selected_resignation_reason=None):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    # Convert months to their respective indices if needed
    if isinstance(selected_months, int):
        selected_months = [selected_months]

    if selected_months and isinstance(selected_months[0], str):
        month_indices = [months.index(month) + 1 for month in selected_months]
    else:
        month_indices = selected_months

    # Process Employees on Resignation report
    if report_type == "Employees on Resignation":
        if org_id is None:
            data = EmpResigantionModel.objects.filter(IsDelete=False)
        else: 
            data = EmpResigantionModel.objects.filter(OrganizationID=org_id, IsDelete=False)    

        work_departmentorg = Subquery(OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1])
        work_departmentorg_id = Subquery(
            OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
        )

        
        emp_id_subquery = Subquery(
            EmployeePersonalDetails.objects.filter(
                EmployeeCode=OuterRef('Emp_Code'),
                IsDelete=False
            ).values('EmpID')[:1]
        )
        # if selected_Division != 'All':
        #     data = data.filter(Dept=selected_Division)
        if selected_Division != 'All':
            # print("the selected division is here", selected_Division)
            data = data.filter(Division=selected_Division)
            
        if selected_department != 'All':
            # print("the selected department is here", selected_department)
            data = data.filter(Dept=selected_department)


        if selected_designation != 'All':
            data = data.filter(Designation=selected_designation)

        if selected_resignation_reason and selected_resignation_reason != 'All':
            data = data.filter(Res_Reason=selected_resignation_reason)

        data = data.annotate(work_departmentorg=work_departmentorg, work_departmentorg_id=work_departmentorg_id,
            EmpID=emp_id_subquery)
        data = data.filter(Date_Of_res__year__in=selected_year, Date_Of_res__month__in=month_indices)

        columns_order = ['work_departmentorg','Name', 'Emp_Code', 'Dept', 'Designation','work_departmentorg_id','EmpID', 
                         'DOJ', 'Date_Of_res', 'Res_Reason', 'TypeofRes', 'LastWorkingDays']

        # Convert queryset to DataFrame
        data = pd.DataFrame(list(data.values(
             'work_departmentorg','Name', 'Emp_Code', 'Dept', 'Designation','work_departmentorg_id','EmpID', 
             'DOJ', 'Date_Of_res', 'Res_Reason', 'TypeofRes', 'LastWorkingDays'
        )))

        


        if 'work_departmentorg' not in data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            data = data.sort_values(by='work_departmentorg', ascending=True)   

        missing_columns = [col for col in columns_order if col not in data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            data = data[columns_order]
         # Generate URLs with EmpID
        PyHost = MasterAttribute.PyHost
       
        if not data.empty:
            data['View'] = data.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}" if row['EmpID'] else None, axis=1
            )
        else:
            print("The DataFrame is empty.")

    # Process Employees on Termination report
    elif report_type == "Employees on Termination":

        if org_id is None:
            data = EmpTerminationModel.objects.filter(IsDelete=False)
        else: 
            data = EmpTerminationModel.objects.filter(OrganizationID=org_id, IsDelete=False)  
        work_departmentorg = Subquery(OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1])
        work_departmentorg_id = Subquery(
            OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
        )

        
        emp_id_subquery = Subquery(
            EmployeePersonalDetails.objects.filter(
                EmployeeCode=OuterRef('Emp_Code'),
                IsDelete=False
            ).values('EmpID')[:1]
        )
        if selected_department != 'All':
            data = data.filter(Dept=selected_department)

        if selected_designation != 'All':
            data = data.filter(Designation=selected_designation)

        data = data.filter(DOJ__year__in=selected_year, DOJ__month__in=month_indices)
        
        data = data.annotate(work_departmentorg=work_departmentorg, work_departmentorg_id=work_departmentorg_id,
            EmpID=emp_id_subquery)

        columns_order = ['work_departmentorg','Name', 'Emp_Code', 'Dept', 'Designation','work_departmentorg_id','EmpID', 
                         'DOJ', 'Remarks', 'LastWarningLatter']

        data = pd.DataFrame(list(data.values(
            'work_departmentorg','Name', 'Emp_Code', 'Dept', 'Designation','work_departmentorg_id','EmpID', 
            'DOJ', 'Remarks', 'LastWarningLatter'
        )))

        if 'work_departmentorg' not in data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            data = data.sort_values(by='work_departmentorg', ascending=True)   
        
        missing_columns = [col for col in columns_order if col not in data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            data = data[columns_order]
        PyHost = MasterAttribute.PyHost
       
        if not data.empty:
            data['View'] = data.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}" if row['EmpID'] else None, axis=1
            )
        else:
            print("The DataFrame is empty.")

    return data
    


from django.db.models.functions import Concat
from datetime import datetime
import pandas as pd
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Concat

def fetch_new_joinees_data(report_type, org_id, selected_department, selected_designation, selected_year, selected_months, report_options):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "New Joinees Report":
        organization_name = get_organization_short_name(org_id)
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Prepare the work details query
        work_details_filter = {
            'IsDelete': False
        }
        
        if org_id is not None:
            work_details_filter['OrganizationID'] = org_id

        work_details = EmployeeWorkDetails.objects.filter(
            EmpID=OuterRef('EmpID'),
            **work_details_filter
        )

        # Create the employee queryset with necessary annotations
        employees = EmployeePersonalDetails.objects.annotate(
            work_designation=Subquery(work_details.values('Designation')[:1]),
            work_department=Subquery(work_details.values('Department')[:1]),
            work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
            work_status=Subquery(work_details.values('EmpStatus')[:1]),
            work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
            work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
            ),
            full_name=Concat('FirstName', Value(' '), 'LastName')
        ).filter(IsDelete=False)

        # Apply filters based on selected department and designation
        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)
        
        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        # Filter by work status and joining date
        valid_statuses = ["On Probation"]
        employees = employees.filter(
            work_status__in=valid_statuses,
            work_date_of_joining__year=current_year,
            work_date_of_joining__month=current_month
        )

        # Filter by selected year and months
        employees = employees.filter(
            work_date_of_joining__year__in=selected_year,
            work_date_of_joining__month__in=[months.index(month) + 1 for month in selected_months]
        )

        # Define the column order for the output
        columns_order = ['work_departmentorg', 'EmployeeCode', 'full_name', 'work_department','work_departmentorg_id','EmpID',
                         'work_designation', 'work_date_of_joining', 'work_status']

        # Create DataFrame from employees values
        data = pd.DataFrame(list(employees.values(
            'work_departmentorg', 'full_name', 'EmployeeCode', 'work_department','work_departmentorg_id','EmpID',
            'work_designation', 'work_date_of_joining', 'work_status',
            'EmpID', 'work_departmentorg_id'  # Add necessary fields here
        )))

        # Check if all the required columns are present
        missing_columns = [col for col in columns_order if col not in data.columns]
        
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            # Reorder columns if no missing columns
            data = data[columns_order]

        # Add 'View' column with the correct URL
        PyHost = MasterAttribute.PyHost
        if not data.empty:
            data['View'] = data.apply(
                lambda row: f"{PyHost}HumanResources/EditEmployee/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
            )
        else:
            print("The DataFrame is empty.")


        return data

    return None




def fetch_confirmation_letters_data(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Pending Confirmation Letters":
        # Define work details filter
        work_details_filter = {
            "EmpID": OuterRef("EmpID"),
            "IsDelete": False
        }
        if org_id:
            work_details_filter["OrganizationID"] = org_id

        work_details = EmployeeWorkDetails.objects.filter(**work_details_filter)

        employees = EmployeePersonalDetails.objects.annotate(
            work_designation=Subquery(work_details.values("Designation")[:1]),
            work_department=Subquery(work_details.values("Department")[:1]),
            work_date_of_joining=Subquery(work_details.values("DateofJoining")[:1]),
            work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                OrganizationID=OuterRef("OrganizationID"),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
            work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
            ),
            work_status=Subquery(work_details.values("EmpStatus")[:1]),
            full_name=Concat("FirstName", Value(" "), "LastName")
        ).filter(IsDelete=False)

        # Apply organization ID filter
        if org_id:
            employees = employees.filter(OrganizationID=org_id)

        # Apply department and designation filters
        if selected_department != "All":
            employees = employees.filter(work_department=selected_department)

        if selected_designation != "All":
            employees = employees.filter(work_designation=selected_designation)

        # Filter by valid statuses
        valid_statuses = ["On Probation", "Not Confirmed"]
        employees = employees.filter(work_status__in=valid_statuses)

        # Exclude invalid employee codes
        employees = employees.exclude(EmployeeCode__isnull=True).exclude(EmployeeCode__exact="")

        # Convert queryset to DataFrame
                # Convert queryset to DataFrame
        emp_df = pd.DataFrame(list(employees.values(
            "work_departmentorg", "full_name", "EmployeeCode",
            "work_department", "work_designation",'work_departmentorg_id','EmpID',
            "work_date_of_joining", "work_status"
        )))
        # emp_df = emp_df.sort_values(by='work_departmentorg', ascending=True)
        if 'work_departmentorg' not in emp_df.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            emp_df = emp_df.sort_values(by='work_departmentorg', ascending=True)
        # Reorder columns to ensure 'work_departmentorg' is first
        if not emp_df.empty:  # Check if the DataFrame is not empty
            columns_order = ["work_departmentorg", "full_name", "EmployeeCode",'work_departmentorg_id','EmpID',
                             "work_department", "work_designation",
                             "work_date_of_joining", "work_status"]
            emp_df = emp_df[columns_order]

        today = timezone.now().date()

        # Handle missing 'work_date_of_joining'
        if "work_date_of_joining" not in emp_df.columns:
            emp_df["work_date_of_joining"] = None

        # Calculate Date of Confirmation
        emp_df["Date of Confirmation"] = emp_df["work_date_of_joining"].apply(
            lambda x: x + timedelta(days=180) if pd.notnull(x) else None
        )

        # Calculate Remaining Days
        def calculate_remaining_days(date_of_confirmation):
            if date_of_confirmation:
                days_diff = (date_of_confirmation - today).days
                if days_diff < 0:
                    return f"Pending since {abs(days_diff)} days"
                elif days_diff == 0:
                    return "Due Today"
                else:
                    return "Not due yet"
            return ""

        emp_df["Remaining Days"] = emp_df["Date of Confirmation"].apply(calculate_remaining_days)

        # Filter rows with 'Pending' in Remaining Days
        emp_df = emp_df[emp_df["Remaining Days"].str.contains("Pending", na=False)]
        PyHost = MasterAttribute.PyHost
       
        if not emp_df.empty:
            emp_df['View'] = emp_df.apply(
            lambda row: f"{PyHost}HumanResources/EditEmployee/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
            )
        else:
            print("The DataFrame is empty.")

        return emp_df



def fetch_new_Emergency_data(report_type,report_options, org_id,selected_Division, selected_department, selected_designation,selected_year, selected_months):
    
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    if report_type == "Emergency Contact Report":
        if org_id is None:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                
            )

            Emerg_details = EmployeeEmergencyInformationDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_division=Subquery(work_details.values('Division')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                    
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                emergency_first_name=Subquery(Emerg_details.values('FirstName')[:1]),
                emergency_middle_name=Subquery(Emerg_details.values('MiddleName')[:1]),
                emergency_last_name=Subquery(Emerg_details.values('LastName')[:1]),
                emergency_relation=Subquery(Emerg_details.values('Relation')[:1]),
                emergency_contact_1=Subquery(Emerg_details.values('EmergencyContactNumber_1')[:1]),
                emergency_contact_2=Subquery(Emerg_details.values('EmergencyContactNumber_2')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False)
        else:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

            Emerg_details = EmployeeEmergencyInformationDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_division=Subquery(work_details.values('Division')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                    
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                emergency_first_name=Subquery(Emerg_details.values('FirstName')[:1]),
                emergency_middle_name=Subquery(Emerg_details.values('MiddleName')[:1]),
                emergency_last_name=Subquery(Emerg_details.values('LastName')[:1]),
                emergency_relation=Subquery(Emerg_details.values('Relation')[:1]),
                emergency_contact_1=Subquery(Emerg_details.values('EmergencyContactNumber_1')[:1]),
                emergency_contact_2=Subquery(Emerg_details.values('EmergencyContactNumber_2')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False, OrganizationID=org_id)

        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)

        if selected_Division != 'All':
            employees = employees.filter(work_division=selected_Division)

        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        valid_statuses = ["On Probation","Not Confirmed","Confirmed"]
        employees = employees.filter(work_status__in=valid_statuses)
        employees = employees.exclude(EmployeeCode__isnull=True).exclude(EmployeeCode__exact='')
        employees = employees.filter(work_date_of_joining__year__in=selected_year, work_date_of_joining__month__in=[months.index(month) + 1 for month in selected_months])
      
        employee_data = pd.DataFrame(list(employees.values(
            'work_departmentorg','full_name', 'EmployeeCode', 'work_division',
            'work_department', 'work_designation', 'work_departmentorg_id','EmpID',
            'work_date_of_joining', 'work_status',
            'emergency_first_name',  'emergency_relation', 
            'emergency_contact_1', 'emergency_contact_2'
        )))

        # employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        if 'work_departmentorg' not in employee_data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        columns_order = ['work_departmentorg', 'EmployeeCode', 'full_name', 'work_division',
                        'work_department', 'work_designation', 'work_departmentorg_id','EmpID',
                        'work_date_of_joining', 'work_status', 'emergency_first_name',  
                        'emergency_relation', 'emergency_contact_1', 'emergency_contact_2']

        
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            
            employee_data = employee_data[columns_order]

        PyHost = MasterAttribute.PyHost
        
        if not employee_data.empty:
            employee_data['View'] = employee_data.apply(
            lambda row: f"{PyHost}HumanResources/EditEmployee/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
            )
        else:
            print("The DataFrame is empty.")  

        return employee_data




#This is blood report function
def fetch_blood_data(report_type, report_options, org_id, selected_Division, selected_department, selected_designation,selected_year, selected_months,):
    
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    
    if report_type == "Blood Group Report":
        if org_id is None:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
            )

            Emerg_details = EmployeeEmergencyInformationDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_ReportingToDesignation=Subquery(work_details.values('ReportingtoDesignation')[:1]),
                work_division=Subquery(work_details.values('Division')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                         
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                emergency_first_name=Subquery(Emerg_details.values('FirstName')[:1]),
                emergency_middle_name=Subquery(Emerg_details.values('MiddleName')[:1]),
                emergency_last_name=Subquery(Emerg_details.values('LastName')[:1]),
                Blood_Group=Subquery(Emerg_details.values('BloodGroup')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')

            ).filter(IsDelete=False)
        else:    
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

        
            Emerg_details = EmployeeEmergencyInformationDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

        
            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_ReportingToDesignation=Subquery(work_details.values('ReportingtoDesignation')[:1]),
                work_division=Subquery(work_details.values('Division')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                         
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                emergency_first_name=Subquery(Emerg_details.values('FirstName')[:1]),
                emergency_middle_name=Subquery(Emerg_details.values('MiddleName')[:1]),
                emergency_last_name=Subquery(Emerg_details.values('LastName')[:1]),
                Blood_Group=Subquery(Emerg_details.values('BloodGroup')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False, OrganizationID=org_id)

        if selected_Division != 'All':
            employees = employees.filter(work_division=selected_Division)

        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)

        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        valid_statuses = ["On Probation","Not Confirmed","Confirmed"]
        employees = employees.filter(work_status__in=valid_statuses)
        employees = employees.exclude(EmployeeCode__isnull=True).exclude(EmployeeCode__exact='')    
        employees = employees.filter(work_date_of_joining__year__in=selected_year, work_date_of_joining__month__in=[months.index(month) + 1 for month in selected_months])
       # Define the list of columns you want
        columns_order = ['work_departmentorg', 'EmployeeCode', 'full_name', 'work_division',
                        'work_department', 'work_designation','work_ReportingToDesignation', 'work_departmentorg_id','EmpID',
                        'work_date_of_joining', 'work_status', 'Blood_Group']

        # Create DataFrame from employees values
        employee_data = pd.DataFrame(list(employees.values(
            'work_departmentorg', 'full_name', 'EmployeeCode', 'work_division',
            'work_department', 'work_designation','work_ReportingToDesignation', 'work_departmentorg_id','EmpID',
            'work_date_of_joining', 'work_status', 'Blood_Group'
        )))
        # employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        if 'work_departmentorg' not in employee_data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        # Check if all the required columns are in the DataFrame
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        # If there are missing columns, print a message and avoid raising an error
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            # If no columns are missing, proceed with reordering
            employee_data = employee_data[columns_order]
        PyHost = MasterAttribute.PyHost
          
        if not employee_data.empty:
            employee_data['View'] = employee_data.apply(
            lambda row: f"{PyHost}HumanResources/EmergencyInfoPage/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
            )
        else:
            print("The DataFrame is empty.")  
  
        return employee_data


#This fetch_Locker_Allotment_data
def fetch_Locker_Allotment_data_Two(report_type, report_options, org_id, selected_Division, selected_department, selected_designation,selected_year, selected_months,):
    
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    
    if report_type == "Blood Group Report":
        if org_id is None:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
            )

            Emerg_details = EmployeeEmergencyInformationDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_ReportingToDesignation=Subquery(work_details.values('ReportingtoDesignation')[:1]),
                work_division=Subquery(work_details.values('Division')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                         
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                emergency_first_name=Subquery(Emerg_details.values('FirstName')[:1]),
                emergency_middle_name=Subquery(Emerg_details.values('MiddleName')[:1]),
                emergency_last_name=Subquery(Emerg_details.values('LastName')[:1]),
                Blood_Group=Subquery(Emerg_details.values('BloodGroup')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')

            ).filter(IsDelete=False)
        else:    
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

        
            Emerg_details = EmployeeEmergencyInformationDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

        
            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_ReportingToDesignation=Subquery(work_details.values('ReportingtoDesignation')[:1]),
                work_division=Subquery(work_details.values('Division')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                         
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                emergency_first_name=Subquery(Emerg_details.values('FirstName')[:1]),
                emergency_middle_name=Subquery(Emerg_details.values('MiddleName')[:1]),
                emergency_last_name=Subquery(Emerg_details.values('LastName')[:1]),
                Blood_Group=Subquery(Emerg_details.values('BloodGroup')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False, OrganizationID=org_id)

        if selected_Division != 'All':
            employees = employees.filter(work_division=selected_Division)

        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)

        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        valid_statuses = ["On Probation","Not Confirmed","Confirmed"]
        employees = employees.filter(work_status__in=valid_statuses)
        employees = employees.exclude(EmployeeCode__isnull=True).exclude(EmployeeCode__exact='')    
        employees = employees.filter(work_date_of_joining__year__in=selected_year, work_date_of_joining__month__in=[months.index(month) + 1 for month in selected_months])
       # Define the list of columns you want
        columns_order = ['work_departmentorg', 'EmployeeCode', 'full_name', 'work_division',
                        'work_department', 'work_designation','work_ReportingToDesignation', 'work_departmentorg_id','EmpID',
                        'work_date_of_joining', 'work_status', 'Blood_Group']

        # Create DataFrame from employees values
        employee_data = pd.DataFrame(list(employees.values(
            'work_departmentorg', 'full_name', 'EmployeeCode', 'work_division',
            'work_department', 'work_designation','work_ReportingToDesignation', 'work_departmentorg_id','EmpID',
            'work_date_of_joining', 'work_status', 'Blood_Group'
        )))
        # employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        if 'work_departmentorg' not in employee_data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        # Check if all the required columns are in the DataFrame
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        # If there are missing columns, print a message and avoid raising an error
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            # If no columns are missing, proceed with reordering
            employee_data = employee_data[columns_order]
        PyHost = MasterAttribute.PyHost
          
        if not employee_data.empty:
            employee_data['View'] = employee_data.apply(
            lambda row: f"{PyHost}HumanResources/EmergencyInfoPage/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
            )
        else:
            print("The DataFrame is empty.")  
  
        return employee_data




from django.db.models import F, OuterRef, Subquery
import pandas as pd
from django.db.models import OuterRef, Subquery
import pandas as pd

from django.db.models import OuterRef, Subquery
import pandas as pd

import streamlit as st

import pandas as pd
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Concat
import streamlit as st
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from hotelopsmgmtpy.utils import encrypt_id
import random
import pandas as pd
from django.db.models import OuterRef, Subquery

from Manning_Guide.models import EntryActualContract,EntryActualSharedServices,EntryActualMealCost,ManageBudgetSharedServices,BudgetInsuranceCost,EntryActualInsuranceCost,BudgetMealCost,ManageBudgetContract


def fetch_absconding_data(report_type, report_options, org_id, selected_department, selected_designation, selected_year, selected_months):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Absconding Employees Report":
        if org_id is None:
            absconding_employees = EmpAbscondingModel.objects.filter(IsDelete=False)
        else:
            absconding_employees = EmpAbscondingModel.objects.filter(OrganizationID=org_id, IsDelete=False)

       
        if selected_department != 'All':
            absconding_employees = absconding_employees.filter(Dept=selected_department)

        if selected_designation != 'All':
            absconding_employees = absconding_employees.filter(Designation=selected_designation)

        
        absconding_employees = absconding_employees.filter(
            DOJ__year__in=selected_year,
            DOJ__month__in=[i + 1 for i, month in enumerate(selected_months)]
        )

       
        work_departmentorg = Subquery(OrganizationMaster.objects.filter(
            OrganizationID=OuterRef('OrganizationID'),
            IsDelete=False
        ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1])

        work_departmentorg_id = Subquery(
            OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
        )

        
        emp_id_subquery = Subquery(
            EmployeePersonalDetails.objects.filter(
                EmployeeCode=OuterRef('Emp_Code'),
                IsDelete=False
            ).values('EmpID')[:1]
        )

        absconding_employees = absconding_employees.annotate(
            work_departmentorg=work_departmentorg,
            work_departmentorg_id=work_departmentorg_id,
            EmpID=emp_id_subquery
        )
        
       
        columns_order = [
            'work_departmentorg', 'Emp_Code', 'Name', 'Dept', 'Designation', 'work_departmentorg_id',
            'DOJ', 'Date_Of_Absconding', 'Remarks', 'EmpID'
        ]

        absconding_employees = pd.DataFrame(list(absconding_employees.values(
            'work_departmentorg', 'Emp_Code', 'Name', 'Dept', 'Designation', 'work_departmentorg_id',
            'DOJ', 'Date_Of_Absconding', 'Remarks', 'EmpID'
        )))

        
        if 'work_departmentorg' not in absconding_employees.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            absconding_employees = absconding_employees.sort_values(by='work_departmentorg', ascending=True)   
      
        missing_columns = [col for col in columns_order if col not in absconding_employees.columns]
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            absconding_employees = absconding_employees[columns_order]

        
        PyHost = MasterAttribute.PyHost
        
        if not absconding_employees.empty:
           absconding_employees['View'] = absconding_employees.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}" if row['EmpID'] else None, axis=1
           )
        else:
            print("The DataFrame is empty.")

        return absconding_employees



def fetch_TerminateEmployees_data(report_type, report_options, org_id, selected_department, selected_designation, selected_year, selected_months):
    
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    
    if report_type == "Terminated Employees":
        
        
        EmpTermination = EmpTerminationModel.objects.filter(IsDelete=False)
        
          

        
        work_departmentorg = Subquery(OrganizationMaster.objects.filter(
            OrganizationID=OuterRef('OrganizationID'),
            IsDelete=False
        ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1])

       
        if selected_department != 'All':
            EmpTermination = EmpTermination.filter(Dept=selected_department)

        
        if selected_designation != 'All':
            EmpTermination = EmpTermination.filter(Designation=selected_designation)

        
        EmpTermination = EmpTermination.filter(
            DOJ__year__in=selected_year,
            DOJ__month__in=[i + 1 for i, month in enumerate(selected_months)]
        )

        
        EmpTermination = EmpTermination.annotate(work_departmentorg=work_departmentorg)

       
        columns_order = ['work_departmentorg',  'Name', 'Dept', 'Designation',
            'Date_Of_Termination', 'Remarks']

        
        EmpTermination = pd.DataFrame(list(EmpTermination.values(
           'work_departmentorg',  'Name', 'Dept', 'Designation',
            'Date_Of_Termination',  'Remarks'
        )))
        # EmpTermination = EmpTermination.sort_values(by='work_departmentorg', ascending=True)
        if 'work_departmentorg' not in EmpTermination.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            EmpTermination = EmpTermination.sort_values(by='work_departmentorg', ascending=True)
        missing_columns = [col for col in columns_order if col not in EmpTermination.columns]

        
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
           
            EmpTermination = EmpTermination[columns_order]
        
        return EmpTermination




def fetch_Birthdays_data(report_type, report_options, org_id, selected_year, selected_months, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Upcoming Birthday's report":
        
        
        current_month = datetime.now().month
        if org_id is None:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                          
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False)

        else:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                      
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False, OrganizationID=org_id)
        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)

        
        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

      
        employees = employees.filter(DateofBirth__month__in=[months.index(month) + 1 for month in selected_months])

        
        employees = employees.exclude(DateofBirth__isnull=True)
        employees = employees.filter(
           
            DateofBirth__month=current_month
        )
        valid_statuses = ["On Probation","Not Confirmed","Confirmed"]
        employees = employees.filter(work_status__in=valid_statuses)
        employees = employees.exclude(EmployeeCode__isnull=True).exclude(EmployeeCode__exact='')   

       
        columns_order = ['work_departmentorg','EmployeeCode','full_name','work_departmentorg_id','EmpID',  
                        'work_department', 'work_designation', 'work_status', 'DateofBirth']

       
        employee_data = pd.DataFrame(list(employees.values(
            'work_departmentorg','EmployeeCode', 'full_name', 'work_departmentorg_id','EmpID',
            'work_department', 'work_designation', 'work_status', 'DateofBirth'
        )))
        # employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        if 'work_departmentorg' not in employee_data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            
            employee_data = employee_data[columns_order]

        PyHost = MasterAttribute.PyHost
      
        if not employee_data.empty:
            employee_data['View'] = employee_data.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
             )
        else:
            print("The DataFrame is empty.")   
        return employee_data



def fetch_Acutalcounthr(report_type, report_options, org_id, selected_year, selected_months, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Actual Salary OnRoll Report":
        
        
       
        if org_id is None:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_Salary=Subquery(work_details.values('Salary')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
               
                
            ).filter(IsDelete=False)

        else:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_Salary=Subquery(work_details.values('Salary')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
               
            ).filter(IsDelete=False, OrganizationID=org_id)
        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)

        
        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

      
       
        
       
       
       

       
        columns_order = ['work_departmentorg',
                        'work_department', 'work_designation','work_Salary'  ]

       
        employee_data = pd.DataFrame(list(employees.values(
            'work_departmentorg',
            'work_department', 'work_designation',  'work_Salary'
        )))
        
        if 'work_departmentorg' not in employee_data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            # If no columns are missing, proceed with reordering
            employee_data = employee_data[columns_order]

        return employee_data




def fetch_AcutalHeadCounthr(report_type, report_options, org_id, selected_department, selected_designation):
    """
    Fetches the actual headcount data for employees, grouped by organization, department, and designation.
    
    :param report_type: Type of report requested.
    :param report_options: Available report options.
    :param org_id: ID of the organization to filter data.
    :param selected_department: Department to filter data (or 'All').
    :param selected_designation: Designation to filter data (or 'All').
    :return: A Pandas DataFrame containing grouped headcount data.
    """
    # Validate report type
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Actual Head Count OnRoll Report":
        # Subquery for employee work details
        work_details = EmployeeWorkDetails.objects.filter(
            EmpID=OuterRef('EmpID'),
            IsDelete=False,
            **({'OrganizationID': org_id} if org_id else {})
        )

        # Query employee data with annotations
        employees = EmployeePersonalDetails.objects.annotate(
            work_designation=Subquery(work_details.values('Designation')[:1]),
            work_department=Subquery(work_details.values('Department')[:1]),
            work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
        ).filter(IsDelete=False, **({'OrganizationID': org_id} if org_id else {}))

        # Apply department filter if specified
        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)

        # Apply designation filter if specified
        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        # Convert queryset to DataFrame
        employee_data = pd.DataFrame(list(employees.values(
            'work_departmentorg',  # Organization
            'work_department',     # Department
            'work_designation',    # Designation
        )))

        # Check if data is empty
        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return empty DataFrame

        # Group data to eliminate duplicates and calculate headcount
        headcount_data = employee_data.groupby(
            ['work_departmentorg', 'work_department', 'work_designation']
        ).agg(
            head_count=('work_department', 'count')
        ).reset_index()

        # Define the desired column order
        columns_order = ['work_departmentorg', 'work_department', 'work_designation', 'head_count']
        headcount_data = headcount_data[columns_order]

        # Sort the data for better readability
        if 'work_departmentorg' in headcount_data.columns:
            headcount_data = headcount_data.sort_values(by='work_departmentorg', ascending=True)
        else:
            print("Data not found for 'work_departmentorg'")

        # Return the final DataFrame
        return headcount_data



def fetch_ActualContracthr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Actual Contract Report":
        # Initial queryset
        contracts = EntryActualContract.objects.filter(IsDelete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            work_department=F('contract_department_master__DepartmentName'),  # Assuming a 'name' field exists
            work_designation=F('contract_designation_master__designations'),  # Assuming a 'name' field exists
            work_division=F('contract_division_master__DivisionName'),  # Assuming a 'name' field exists
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

        # Apply filters for department and designation
        if selected_department != 'All':
            contracts = contracts.filter(work_department=selected_department)

        if selected_designation != 'All':
            contracts = contracts.filter(work_designation=selected_designation)

        # Convert to DataFrame
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  # Organization
            'work_division',  # Division
            'work_department',  # Department
            'work_designation',  # Designation
            'avg_salary',  # Average Salary
            'head_count',  # Head Count
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found

        # Organize the data
        employee_data['total_ctc'] = employee_data['avg_salary'] * employee_data['head_count']

        # Sort by organization and division
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg', 'work_division'], ascending=True)
        else:
            print("Data not found for 'work_departmentorg'")

        # Ensure columns are in the correct order
        columns_order = [
            'work_departmentorg', 'work_division', 'work_department',
            'work_designation', 'avg_salary', 'head_count', 'total_ctc'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data


def fetch_ActualSharedServiceshr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Actual Shared Services":
        # Initial queryset
        contracts = EntryActualSharedServices.objects.filter(IsDelete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            work_department=F('services_department_master__DepartmentName'),
            work_designation=F('services_designation_master__designations'),
            work_division=F('services_division_master__DivisionName'),
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

        # Apply filters for department and designation
        if selected_department != 'All':
            contracts = contracts.filter(services_department_master__DepartmentName=selected_department)

        if selected_designation != 'All':
            contracts = contracts.filter(services_designation_master__designations=selected_designation)

        # Convert to DataFrame
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  # Organization
                 # Division
            'work_department',     # Department
            'work_designation',    # Designation
            'avg_salary',          # Average Salary
            'head_count',          # Head Count
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found

        # Organize the data
        employee_data['total_ctc'] = employee_data['avg_salary'] * employee_data['head_count']

        # Sort by organization and division
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg', ], ascending=True)
     
        # Ensure columns are in the correct order
        columns_order = [
            'work_departmentorg',  'work_department',
            'work_designation', 'avg_salary', 'head_count', 'total_ctc'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data

       
       

       


def fetch_ActualMealCosthr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Actual Meal Cost":
        # Initial queryset
        contracts = EntryActualMealCost.objects.filter(IsDelete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

       

        # Convert to DataFrame
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  # Organization
                 # Division
           
            'cafeteriamealcost',          # Head Count
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found
           # Convert `work_departmentorg` to uppercase
        if 'work_departmentorg' in employee_data.columns:
            employee_data['work_departmentorg'] = employee_data['work_departmentorg'].str.upper()
      
        # Sort by organization and division
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg', ], ascending=True)

        
        columns_order = [
            'work_departmentorg',   'cafeteriamealcost'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data

def fetch_ActualInsuranceCosthr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Actual Insurance Cost":
        # Initial queryset
        contracts = EntryActualInsuranceCost.objects.filter(IsDelete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

       

        # Convert to DataFrame
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  # Organization
                 # Division
           
            'EmployeeInsurancecost',          # Head Count
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found

        if 'work_departmentorg' in employee_data.columns:
            employee_data['work_departmentorg'] = employee_data['work_departmentorg'].str.upper()
      
        # Sort by organization and division
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg', ], ascending=True)

        # Ensure columns are in the correct order
        columns_order = [
            'work_departmentorg',   'EmployeeInsurancecost'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data




def fetch_BudgetOnRollhr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Budget On Roll Report":
        # Initial queryset
        contracts = ManageBudgetOnRoll.objects.filter(is_delete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            work_department=F('on_roll_department_master__DepartmentName'),
            work_designation=F('on_roll_designation_master__designations'),
            work_division=F('on_roll_division_master__DivisionName'),
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('hotel_name'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

        # Apply filters for department and designation
        if selected_department != 'All':
            contracts = contracts.filter(on_roll_department_master__DepartmentName=selected_department)

        if selected_designation != 'All':
            contracts = contracts.filter(on_roll_designation_master__designations=selected_designation)

        # Convert to DataFrame
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  
            'work_department',     # Department
            'work_designation',    # Designation
            'avg_salary',          # Average Salary
            'head_count',          # Head Count
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found
        if 'work_departmentorg' in employee_data.columns:
            employee_data['work_departmentorg'] = employee_data['work_departmentorg'].str.upper()
      
        # Calculate total CTC
        employee_data['total_ctc'] = employee_data['avg_salary'] * employee_data['head_count']

        # Group by unique fields to remove duplicates
        group_by_columns = ['work_departmentorg', 'work_department', 'work_designation']
        numeric_columns = ['avg_salary', 'head_count', 'total_ctc']

        employee_data = employee_data.groupby(group_by_columns, as_index=False).agg({
            'avg_salary': 'mean',  # Calculate mean for average salary
            'head_count': 'sum',   # Sum up headcounts
            'total_ctc': 'sum'     # Sum up total CTC
        })

        # Sort by organization
       
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg'], ascending=True)

        # Ensure columns are in the correct order
        columns_order = [
            'work_departmentorg', 'work_department',
            'work_designation', 'avg_salary', 'head_count', 'total_ctc'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data



def fetch_BudgetContracthr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Budget Contract Report":
        # Initial queryset
        contracts = ManageBudgetContract.objects.filter(IsDelete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            work_department=F('contract_department_master__DepartmentName'),
            work_designation=F('contract_designation_master__designations'),
            work_division=F('contract_division_master__DivisionName'),
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('hotel_name'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

        # Apply filters for department and designation
        if selected_department != 'All':
            contracts = contracts.filter(contract_department_master__DepartmentName=selected_department)

        if selected_designation != 'All':
            contracts = contracts.filter(contract_designation_master__designations=selected_designation)

        # Convert to DataFrame
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  
                
            'work_department',     # Department
            'work_designation',    # Designation
            'avg_salary',          # Average Salary
            'head_count',          # Head Count
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found

        # Organize the data
        employee_data['total_ctc'] = employee_data['avg_salary'] * employee_data['head_count']

        # Sort by organization and division
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg', ], ascending=True)

        # Ensure columns are in the correct order
        columns_order = [
            'work_departmentorg',  'work_department',
            'work_designation', 'avg_salary', 'head_count', 'total_ctc'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data

def fetch_BudgetMealCosthr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Budget Meal Cost Report":
        # Initial queryset
        contracts = BudgetMealCost.objects.filter(IsDelete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('hotel_name'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

       

       
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  
                 
           
            'cafeteriamealcost',         
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found

      
        # Sort by organization and division
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg', ], ascending=True)

        # Ensure columns are in the correct order
        columns_order = [
            'work_departmentorg',   'cafeteriamealcost'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data
    


def fetch_BudgetInsuranceCosthr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Budget Insurance Cost Report":
        # Initial queryset
        contracts = BudgetInsuranceCost.objects.filter(IsDelete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('hotel_name'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

       

       
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  
                 
           
            'EmployeeInsurancecost',         
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found

      
        # Sort by organization and division
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg', ], ascending=True)

        # Ensure columns are in the correct order
        columns_order = [
            'work_departmentorg',   'EmployeeInsurancecost'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data


def fetch_BudgetSharedServiceshr(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Budget Shared Services Report":
        # Initial queryset
        contracts = ManageBudgetSharedServices.objects.filter(IsDelete=False)

        # Filter by organization ID if provided
        if org_id:
            contracts = contracts.filter(OrganizationID=org_id)

        # Annotate related fields, including organization short display label
        contracts = contracts.annotate(
            work_department=F('services_department_master__DepartmentName'),
            work_designation=F('services_designation_master__designations'),
            work_division=F('services_division_master__DivisionName'),
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('hotel_name'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            )
        )

        # Apply filters for department and designation
        if selected_department != 'All':
            contracts = contracts.filter(services_department_master__DepartmentName=selected_department)

        if selected_designation != 'All':
            contracts = contracts.filter(services_designation_master__designations=selected_designation)

        # Convert to DataFrame
        employee_data = pd.DataFrame(list(contracts.values(
            'work_departmentorg',  # Organization
                 # Division
            'work_department',     # Department
            'work_designation',    # Designation
            'avg_salary',          # Average Salary
            'head_count',          # Head Count
        )))

        if employee_data.empty:
            print("No data found for the given filters.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is found

        # Organize the data
        employee_data['total_ctc'] = employee_data['avg_salary'] * employee_data['head_count']

        # Sort by organization and division
        if 'work_departmentorg' in employee_data.columns:
            employee_data = employee_data.sort_values(by=['work_departmentorg', ], ascending=True)

        # Ensure columns are in the correct order
        columns_order = [
            'work_departmentorg',  'work_department',
            'work_designation', 'avg_salary', 'head_count', 'total_ctc'
        ]
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        return employee_data




def fetch_probation_data(report_type, report_options, org_id, selected_department, selected_designation, selected_year, selected_months):
    # Validate report type
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees on Probation":
        # Filter work details for employees on probation
        work_details = EmployeeWorkDetails.objects.filter(
            EmpID=OuterRef('EmpID'),
            IsDelete=False,
            EmpStatus='On Probation'
        )
        if org_id:
            work_details = work_details.filter(OrganizationID=org_id)

        # Fetch employee details with annotations for work details
        employees = EmployeePersonalDetails.objects.annotate(
            work_designation=Subquery(work_details.values('Designation')[:1]),
            work_department=Subquery(work_details.values('Department')[:1]),
            work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
            work_status=Subquery(work_details.values('EmpStatus')[:1]),
            work_departmentorg=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]
            ),
            work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
            ),
            full_name=Concat('FirstName', Value(' '), 'LastName')
        ).filter(IsDelete=False)

        # Apply filters
        if org_id:
            employees = employees.filter(OrganizationID=org_id)
        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)
        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        # Filter by joining year and month
        employees = employees.filter(
            work_date_of_joining__year__in=selected_year,
            work_date_of_joining__month__in=[month if isinstance(month, int) else selected_months.index(month) + 1 for month in selected_months]
        )

        # Convert queryset to DataFrame
        employee_data = pd.DataFrame(list(employees.values(
            'work_departmentorg', 'full_name', 'EmployeeCode', 'EmpID',
            'work_department', 'work_designation', 'work_departmentorg_id',
            'work_date_of_joining', 'work_status'
        )))
        
        columns_order = [
            'work_departmentorg', 'full_name', 'EmployeeCode', 'EmpID',
            'work_department', 'work_designation', 'work_departmentorg_id',
            'work_date_of_joining', 'work_status'
        ]
        
        missing_columns = [col for col in columns_order if col not in employee_data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[columns_order]

        if 'work_departmentorg' not in employee_data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            employee_data = employee_data.sort_values(by='work_departmentorg', ascending=True)

        if employee_data.empty:
            st.write("No employees found for the selected filters.")
            return pd.DataFrame()
        employee_data['work_date_of_joining'] = employee_data['work_date_of_joining'].apply(format_date)
        employee_data = employee_data.rename(columns={
            'EmpID': 'EmpID',
            'full_name': 'Name',
            'work_departmentorg': 'Hotel Name',
            'EmployeeCode': 'Emp Code',
            'work_department': 'Department',
            'work_designation': 'Designation',
            'work_date_of_joining': 'Date of Joining',
            'work_status': 'Status',
        })

        PyHost = MasterAttribute.PyHost
       
        if not employee_data.empty:
            employee_data['View'] = employee_data.apply(
            lambda row: f"{PyHost}HumanResources/EditEmployee/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
            )
        else:
            print("The DataFrame is empty.")   
        
        df_display = employee_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1

        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        
        return employee_data






def fetch_Notice_data(report_type,report_options,org_id,selected_department, selected_designation,selected_year, selected_months):
    
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    
    if report_type == "Employees Serving Notice Period":
        
        if org_id is None:
            data = EmpResigantionModel.objects.filter(IsDelete=False)
        else:
            data = EmpResigantionModel.objects.filter(OrganizationID=org_id, IsDelete=False)

        work_departmentorg = Subquery(OrganizationMaster.objects.filter(
            OrganizationID=OuterRef('OrganizationID'),
            IsDelete=False
        ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1])

        work_departmentorg_id = Subquery(
            OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
        )

        
        emp_id_subquery = Subquery(
            EmployeePersonalDetails.objects.filter(
                EmployeeCode=OuterRef('Emp_Code'),
                IsDelete=False
            ).values('EmpID')[:1]
        )
      
        if selected_department != 'All':
            data = data.filter(Dept=selected_department)

       
        if selected_designation != 'All':
            data = data.filter(Designation=selected_designation)

        
        data = data.filter(DOJ__year__in=selected_year, DOJ__month__in=[months.index(month) + 1 for month in selected_months])
        data = data.annotate(
            work_departmentorg=work_departmentorg,
            work_departmentorg_id=work_departmentorg_id,
            EmpID=emp_id_subquery
        )
      
        columns_order = ['work_departmentorg_id','EmpID','work_departmentorg','Name', 'Emp_Code', 'Dept', 'Designation','DOJ', 
             'Date_Of_res', 'NoticePeriod',]

        data = pd.DataFrame(list(data.values(
            'Name', 'Emp_Code', 'Dept', 'Designation','DOJ', 
             'Date_Of_res', 'NoticePeriod','work_departmentorg_id','EmpID','work_departmentorg'
        )))

        if 'work_departmentorg' not in data.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            data = data.sort_values(by='work_departmentorg', ascending=True)   
        
        missing_columns = [col for col in columns_order if col not in data.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            data = data[columns_order]
        PyHost = MasterAttribute.PyHost
        
        if not data.empty:
           data['View'] = data.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}" if row['EmpID'] else None, axis=1
            )
        else:
            print("The DataFrame is empty.")   
    return data


from HumanResources.views import EmployeeNameandDesignation
import pandas as pd
from app.models import EmployeeMaster
from django.db.models import Count




from django.db.models import Count
from django.db.models.functions import TruncMonth,TruncYear
import pandas as pd
from Manning_Guide.models import ManageBudgetOnRoll
from django.db.models import Count, OuterRef, Subquery
import pandas as pd

def fetch_departmentmanning_names(report_type, report_options, org_id, selected_department, selected_designation):
    """
    Fetch department-wise manning data based on the report type and organization ID.
    Returns the count of employees per department, excluding empty or null departments/designations,
    along with the corresponding organization short label as the first column.
    """
    # Validate report type
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    if report_type == "Department wise manning report":
        # Filter employees by organization ID if provided
        if org_id is None:
            manning = EmployeeWorkDetails.objects.filter(IsDelete=False)
        else:
            manning = EmployeeWorkDetails.objects.filter(OrganizationID=org_id, IsDelete=False)
        
        # Subquery to fetch the organization short label (work_departmentorg)
        work_departmentorg = Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1])

        # Exclude null or empty departments and designations
        manning = manning.exclude(Department__isnull=True).exclude(Department="")
        manning = manning.exclude(Designation__isnull=True).exclude(Designation="")
        
        # Filter by selected department if not 'All'
        if selected_department != 'All':
            manning = manning.filter(Department=selected_department)

        # Filter by selected designation if not 'All'
        if selected_designation != 'All':
            manning = manning.filter(Designation=selected_designation)

        # Annotate with employee count and include the organization short label
        department_counts = manning.values('Department') \
                                   .annotate(employee_count=Count('id')) \
                                   .annotate(work_departmentorg=work_departmentorg)  # Adding organization short label

        # Convert the queryset to a DataFrame
        department_counts_df = pd.DataFrame(department_counts)

        # Check if the required columns exist before reordering
        required_columns = ['work_departmentorg', 'Department', 'employee_count']
        existing_columns = [col for col in required_columns if col in department_counts_df.columns]
        
        # Reorder only if all required columns exist
        if set(existing_columns) == set(required_columns):
            department_counts_df = department_counts_df[existing_columns]
        else:
            print("Some required columns are missing. Existing columns:", department_counts_df.columns)

        return department_counts_df






# def fetch_budget_on_roll_data(report_type, report_options, org_id, selected_department, selected_designation):
#     """
#     Fetch budget data from ManageBudgetOnRoll, grouped by department and designation,
#     and return the employee count and other necessary fields, including monthly and yearly join and resignation data.
#     """
#     if report_type not in report_options:
#         raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
#     if report_type == "Attrition Report":
#         if org_id is None:
#            data = ManageBudgetOnRoll.objects.filter(is_delete=False)
#         else:
#             data = ManageBudgetOnRoll.objects.filter(hotel_name=org_id, is_delete=False)
#         if selected_department != 'All':
#             data = data.filter(on_roll_department_master__DepartmentName=selected_department)
        
#         if selected_designation != 'All':
#             data = data.filter(on_roll_designation_master__DesignationName=selected_designation)
        
#         department_counts = (
#             data
#             .values('on_roll_department_master__DepartmentName')
#             .annotate(budget=Count('id'))
#         )
        
#         budget_df = pd.DataFrame(list(department_counts))
#         if budget_df.empty:
#             return "Data not found"
        
#         budget_df = budget_df.rename(columns={
#             'on_roll_department_master__DepartmentName': 'Department',
#             'budget': 'Budget'
#         })

#         if org_id is None:
#            employee_data = EmployeeWorkDetails.objects.filter(IsDelete=False)
#         else:
#             employee_data = EmployeeWorkDetails.objects.filter(OrganizationID=org_id, IsDelete=False)
#         if selected_department != 'All':
#             employee_data = employee_data.filter(Department=selected_department)
        
#         if selected_designation != 'All':
#             employee_data = employee_data.filter(Designation=selected_designation)
        
#         join_counts_monthly = (
#             employee_data
#             .annotate(join_month=TruncMonth('DateofJoining'))
#             .values('Department')
#             .annotate(join_count=Count('EmpID'))
#             .order_by('Department')
#         )

#         join_counts_monthly_df = pd.DataFrame(list(join_counts_monthly))
#         if join_counts_monthly_df.empty:
#             return "Data not found"
        
#         join_counts_monthly_df = join_counts_monthly_df.rename(columns={
#             'join_count': 'Additions (Month)'
#         })

#         if org_id is None:
#             resignation_data = EmpResigantionModel.objects.filter(IsDelete=False)
#         else:
#             resignation_data = EmpResigantionModel.objects.filter(OrganizationID=org_id, IsDelete=False)
#         if selected_department != 'All':
#             resignation_data = resignation_data.filter(Dept=selected_department)
        
#         if selected_designation != 'All':
#             resignation_data = resignation_data.filter(Designation=selected_designation)
        
#         resignation_counts_monthly = (
#             resignation_data
#             .values('Dept')
#             .annotate(resignation_count=Count('id'))
#             .order_by('Dept')
#         )

#         resignation_monthly_df = pd.DataFrame(list(resignation_counts_monthly))
#         if resignation_monthly_df.empty:
#             return "Data not found"
        
#         resignation_monthly_df = resignation_monthly_df.rename(columns={
#             'Dept': 'Department',
#             'resignation_count': 'Separations (Month)'
#         })

      
#         merged_data = pd.merge(budget_df, join_counts_monthly_df, on="Department", how="left")
#         merged_data = pd.merge(merged_data, resignation_monthly_df, on="Department", how="left")
#         merged_data = merged_data.fillna(0)

       
#         merged_data['Attrition (Month %)'] = merged_data.apply(
#             lambda row: (row['Separations (Month)'] / (row['Additions (Month)'] + row['Separations (Month)'])) * 100 if (row['Additions (Month)'] + row['Separations (Month)']) > 0 else 0,
#             axis=1
#         )

#         merged_data['Attrition (Month %)'] = merged_data['Attrition (Month %)'].apply(lambda x: f"{x:.2f}%")

        
#         join_counts_yearly = (
#             employee_data
#             .annotate(join_year=TruncYear('DateofJoining'))
#             .values('Department')
#             .annotate(join_count=Count('EmpID'))
#             .order_by('Department')
#         )

#         join_counts_yearly_df = pd.DataFrame(list(join_counts_yearly))
#         if join_counts_yearly_df.empty:
#             return "Data not found"
        
#         join_counts_yearly_df = join_counts_yearly_df.rename(columns={
#             'join_count': 'Additions (Year)'
#         })

       
#         resignation_counts_yearly = (
#             resignation_data
#             .annotate(resignation_year=TruncYear('Date_Of_res'))
#             .values('Dept')
#             .annotate(resignation_count=Count('id'))
#             .order_by('Dept')
#         )

#         resignation_yearly_df = pd.DataFrame(list(resignation_counts_yearly))
#         if resignation_yearly_df.empty:
#             return "Data not found"
        
#         resignation_yearly_df = resignation_yearly_df.rename(columns={
#             'Dept': 'Department',
#             'resignation_count': 'Separations (Year)'
#         })

       
#         merged_data = pd.merge(merged_data, join_counts_yearly_df, on="Department", how="left")
#         merged_data = pd.merge(merged_data, resignation_yearly_df, on="Department", how="left")
#         merged_data = merged_data.fillna(0)

        
#         merged_data['Closing Balance'] = merged_data['Budget'] + merged_data['Additions (Year)'] - merged_data['Separations (Year)']

        
#         merged_data['Attrition (Year %)'] = merged_data.apply(
#             lambda row: (row['Separations (Year)'] / (row['Additions (Year)'] + row['Separations (Year)'])) * 100 if (row['Additions (Year)'] + row['Separations (Year)']) > 0 else 0,
#             axis=1
#         )

#         merged_data['Attrition (Year %)'] = merged_data['Attrition (Year %)'].apply(lambda x: f"{x:.2f}%")

#         if merged_data.empty:
#             return "Data not found"
        
#         return merged_data.to_dict('records')

def fetch_budget_on_roll_data(report_type, report_options, org_id, selected_department, selected_designation):
    """
    Fetch budget data from ManageBudgetOnRoll, grouped by department and designation,
    and return the employee count and other necessary fields, including monthly and yearly join and resignation data.
    """
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    if report_type == "Attrition Report":
        # Fetch budget data
        budget_data = ManageBudgetOnRoll.objects.filter(is_delete=False)
        if org_id:
            budget_data = budget_data.filter(hotel_name=org_id)
        if selected_department != 'All':
            budget_data = budget_data.filter(on_roll_department_master__DepartmentName=selected_department)
        if selected_designation != 'All':
            budget_data = budget_data.filter(on_roll_designation_master__DesignationName=selected_designation)
        
        department_counts = (
            budget_data
            .values('on_roll_department_master__DepartmentName')
            .annotate(budget=Count('id'))
        )
        
        budget_df = pd.DataFrame(list(department_counts))
        if budget_df.empty:
            return "Data not found"
        
        budget_df = budget_df.rename(columns={
            'on_roll_department_master__DepartmentName': 'Department',
            'budget': 'Budget'
        })
        
        # Fetch employee data
        employee_data = EmployeeWorkDetails.objects.filter(IsDelete=False)
        if org_id:
            employee_data = employee_data.filter(OrganizationID=org_id)
        if selected_department != 'All':
            employee_data = employee_data.filter(Department=selected_department)
        if selected_designation != 'All':
            employee_data = employee_data.filter(Designation=selected_designation)
        
        # Monthly additions
        join_counts_monthly = (
            employee_data
            .annotate(join_month=TruncMonth('DateofJoining'))
            .values('Department')
            .annotate(join_count=Count('EmpID'))
        )
        join_counts_monthly_df = pd.DataFrame(list(join_counts_monthly))
        join_counts_monthly_df = join_counts_monthly_df.rename(columns={
            'join_count': 'Additions (Month)'
        }) if not join_counts_monthly_df.empty else pd.DataFrame(columns=['Department', 'Additions (Month)'])
        
        # Monthly separations
        resignation_data = EmpResigantionModel.objects.filter(IsDelete=False)
        if org_id:
            resignation_data = resignation_data.filter(OrganizationID=org_id)
        if selected_department != 'All':
            resignation_data = resignation_data.filter(Dept=selected_department)
        if selected_designation != 'All':
            resignation_data = resignation_data.filter(Designation=selected_designation)
        
        resignation_counts_monthly = (
            resignation_data
            .values('Dept')
            .annotate(resignation_count=Count('id'))
        )
        resignation_monthly_df = pd.DataFrame(list(resignation_counts_monthly))
        resignation_monthly_df = resignation_monthly_df.rename(columns={
            'Dept': 'Department',
            'resignation_count': 'Separations (Month)'
        }) if not resignation_monthly_df.empty else pd.DataFrame(columns=['Department', 'Separations (Month)'])
        
        # Merge dataframes
        merged_data = pd.merge(budget_df, join_counts_monthly_df, on="Department", how="left")
        merged_data = pd.merge(merged_data, resignation_monthly_df, on="Department", how="left")
        merged_data = merged_data.fillna(0)
        
        # Monthly attrition
        merged_data['Starting Employees (Month)'] = merged_data['Budget']
        merged_data['Ending Employees (Month)'] = (
            merged_data['Budget'] + merged_data['Additions (Month)'] - merged_data['Separations (Month)']
        )
        merged_data['Attrition (Month %)'] = merged_data.apply(
            lambda row: (row['Separations (Month)'] / 
                        ((row['Starting Employees (Month)'] + row['Ending Employees (Month)']) / 2)) * 100 
            if (row['Starting Employees (Month)'] + row['Ending Employees (Month)']) > 0 else 0,
            axis=1
        )
        
        # Yearly additions
        join_counts_yearly = (
            employee_data
            .annotate(join_year=TruncYear('DateofJoining'))
            .values('Department')
            .annotate(join_count=Count('EmpID'))
        )
        join_counts_yearly_df = pd.DataFrame(list(join_counts_yearly))
        join_counts_yearly_df = join_counts_yearly_df.rename(columns={
            'join_count': 'Additions (Year)'
        }) if not join_counts_yearly_df.empty else pd.DataFrame(columns=['Department', 'Additions (Year)'])
        
        # Yearly separations
        resignation_counts_yearly = (
            resignation_data
            .annotate(resignation_year=TruncYear('Date_Of_res'))
            .values('Dept')
            .annotate(resignation_count=Count('id'))
        )
        resignation_yearly_df = pd.DataFrame(list(resignation_counts_yearly))
        resignation_yearly_df = resignation_yearly_df.rename(columns={
            'Dept': 'Department',
            'resignation_count': 'Separations (Year)'
        }) if not resignation_yearly_df.empty else pd.DataFrame(columns=['Department', 'Separations (Year)'])
        
        # Merge yearly data
        merged_data = pd.merge(merged_data, join_counts_yearly_df, on="Department", how="left")
        merged_data = pd.merge(merged_data, resignation_yearly_df, on="Department", how="left")
        merged_data = merged_data.fillna(0)
        
        # Yearly attrition
        merged_data['Starting Employees (Year)'] = merged_data['Budget']
        merged_data['Ending Employees (Year)'] = (
            merged_data['Budget'] + merged_data['Additions (Year)'] - merged_data['Separations (Year)']
        )
        merged_data['Attrition (Year %)'] = merged_data.apply(
            lambda row: (row['Separations (Year)'] / 
                        ((row['Starting Employees (Year)'] + row['Ending Employees (Year)']) / 2)) * 100 
            if (row['Starting Employees (Year)'] + row['Ending Employees (Year)']) > 0 else 0,
            axis=1
        )
        
        # Closing balance
        merged_data['Closing Balance'] = (
            merged_data['Budget'] + merged_data['Additions (Year)'] - merged_data['Separations (Year)']
        )
        
        # Format percentages
        merged_data['Attrition (Month %)'] = merged_data['Attrition (Month %)'].apply(lambda x: f"{x:.2f}%")
        merged_data['Attrition (Year %)'] = merged_data['Attrition (Year %)'].apply(lambda x: f"{x:.2f}%")
        
        # Return as records
        return merged_data.to_dict('records')





def fetch_exit_interview_data(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    if report_type == "Exit Interview Report":
        
        # Filter data based on org_id
        if org_id is None:
            exit_data = Exitinterviewdata.objects.filter(IsDelete=False)
        else:
            exit_data = Exitinterviewdata.objects.filter(OrganizationID=org_id, IsDelete=False)

        # Create a subquery to fetch the work department organization
        work_departmentorg = Subquery(OrganizationMaster.objects.filter(
            OrganizationID=OuterRef('OrganizationID'),
            IsDelete=False
        ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1])
        work_departmentorg_id = Subquery(
            OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
        )
        emp_id_subquery = Subquery(
            EmployeePersonalDetails.objects.filter(
                EmployeeCode=OuterRef('Employee_Code'),
                IsDelete=False
            ).values('EmpID')[:1]
        )

       
        if selected_department != 'All':
            exit_data = exit_data.filter(Department=selected_department)

        
        if selected_designation != 'All':
            exit_data = exit_data.filter(Job_Title=selected_designation)

        
        exit_data = exit_data.annotate(work_departmentorg=work_departmentorg,
                                       work_departmentorg_id=work_departmentorg_id,EmpID=emp_id_subquery)

       
        columns_order = ['work_departmentorg', 'Employee_Code', 'EmpName', 'Job_Title', 'DateofJoining','work_departmentorg_id', 
                         'Department', 'DateofLeaving', 'NoticePeriod', 'Resign','EmpID', 'Termination']

        
        exit_data_df = pd.DataFrame(list(exit_data.values(
            'work_departmentorg', 'Employee_Code', 'EmpName', 'Job_Title', 'DateofJoining', 'work_departmentorg_id',
            'Department', 'DateofLeaving', 'NoticePeriod', 'Resign','EmpID', 'Termination'
        )))

        
        if 'work_departmentorg' not in exit_data_df.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            exit_data_df = exit_data_df.sort_values(by='work_departmentorg', ascending=True)

        # Check if all the required columns are in the DataFrame
        missing_columns = [col for col in columns_order if col not in exit_data_df.columns]

        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            # Reorder the columns if no missing columns
            exit_data_df = exit_data_df[columns_order]
        PyHost = MasterAttribute.PyHost
       
        if not exit_data_df.empty:
            exit_data_df['View'] = exit_data_df.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}" if row['EmpID'] else None, axis=1
             )
        else:
            print("The DataFrame is empty.")   
        return exit_data_df



from Leave_Management_System.models import Leave_Type_Master
import pandas as pd
from django.db import models
from django.db.models import OuterRef, Subquery, F



from django.db.models import F, Subquery, OuterRef, Value
from django.db.models.functions import Concat
import pandas as pd

def fetch_leave_balance_report(report_type, report_options, org_id, selected_department, selected_designation):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    if report_type == "Leave balance report":
        # Query work details and leave balances
        if org_id is None:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
            )
            leave_balances = Emp_Leave_Balance_Master.objects.filter(
                IsDelete=False,
            ).annotate(
                leave_type=F('Leave_Type_Master__Type'),
                balance=F('Balance')
            )
            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                    OrganizationMaster.objects.filter(
                        OrganizationID=OuterRef('OrganizationID'),
                        IsDelete=False
                    ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False)
        else:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )
            leave_balances = Emp_Leave_Balance_Master.objects.filter(
                IsDelete=False,
                OrganizationID=org_id
            ).annotate(
                leave_type=F('Leave_Type_Master__Type'),
                balance=F('Balance')
            )
            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                    OrganizationMaster.objects.filter(
                        OrganizationID=OuterRef('OrganizationID'),
                        IsDelete=False
                    ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False, OrganizationID=org_id)

        # Apply filters for selected department and designation
        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)

        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        # Fetch employee data
        emp_data = list(employees.values(
            'work_departmentorg', 'full_name', 'EmployeeCode', 'work_departmentorg_id', 'EmpID',
            'work_department', 'work_designation', 'work_date_of_joining'
        ))

        # Convert emp_data to a DataFrame
        emp_data_df = pd.DataFrame(emp_data)

        # Add the 'View' column
        PyHost = MasterAttribute.PyHost
        emp_data_df['View'] = emp_data_df.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}" 
            if row['EmpID'] else None,
            axis=1
        )

        # Fetch leave data
        leave_data = list(leave_balances.values('Emp_code', 'leave_type', 'balance'))

        # Organize leave balances by employee code
        leave_dict = {}
        for leave in leave_data:
            emp_code = leave['Emp_code']
            leave_type = leave['leave_type']
            balance = leave['balance']
            if emp_code not in leave_dict:
                leave_dict[emp_code] = {}
            leave_dict[emp_code][leave_type] = balance

        # Add leave balances to employee data
        for emp in emp_data:
            emp_leave_balances = leave_dict.get(emp['EmployeeCode'], {})
            emp.update(emp_leave_balances)

        # Convert the updated emp_data back to a DataFrame
        df = pd.DataFrame(emp_data)

        # Ensure 'work_departmentorg' is in the DataFrame
        if 'work_departmentorg' not in df.columns:
            print("Data not found for 'work_departmentorg'. Cannot generate the report.")
            return pd.DataFrame()  # Return an empty DataFrame if the column is missing

        # Get leave types
        leave_types = Leave_Type_Master.objects.filter(IsDelete=False, Is_Active=True).values_list('Type', flat=True)

        # Ensure all leave types are present in the DataFrame, add columns if necessary
        for leave_type in leave_types:
            if leave_type not in df.columns:
                df[leave_type] = 0

        # Create pivot table to summarize leave balances
        try:
            pivot_table = pd.pivot_table(
                df,
                index=[
                    'work_departmentorg', 'EmployeeCode', 'full_name', 'work_department', 
                    'work_designation', 'work_date_of_joining', 'work_departmentorg_id', 'EmpID'
                ],
                values=[leave_type for leave_type in leave_types if leave_type in df.columns],
                aggfunc='sum',
                fill_value=0
            ).reset_index()

            return pivot_table
        except KeyError as e:
            print(f"Error: Missing key while creating pivot table: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    return pd.DataFrame()




from django.db.models import OuterRef, Subquery, F, Exists, Value
from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail
def fetch_appointment_letters_data(report_type, report_options, org_id, selected_department='All', selected_designation='All'):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Pending appointment letters":
        if org_id is None:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                     
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False)

        else:
            work_details = EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id,
            )

            employees = EmployeePersonalDetails.objects.annotate(
                work_designation=Subquery(work_details.values('Designation')[:1]),
                work_department=Subquery(work_details.values('Department')[:1]),
                work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                                        OrganizationID=OuterRef('OrganizationID'),
                                        IsDelete=False
                                    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                work_departmentorg_id=Subquery(
                OrganizationMaster.objects.filter(
                    OrganizationID=OuterRef('OrganizationID'),
                    IsDelete=False
                ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                ),                       
                work_date_of_joining=Subquery(work_details.values('DateofJoining')[:1]),
                work_status=Subquery(work_details.values('EmpStatus')[:1]),
                full_name=Concat('FirstName', Value(' '), 'LastName')
            ).filter(IsDelete=False, OrganizationID=org_id)
        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)

        
        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        
        appointment_details = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
            emp_code=OuterRef('EmployeeCode'),
            IsDelete=False,
        ).values('date_of_appointment')

        
        employees = employees.annotate(
            date_of_appointment=Subquery(appointment_details[:1]),
            appointment_status=Exists(appointment_details)
        )
     
       
        valid_statuses = ["On Probation", "Not Confirmed", "Confirmed"]
        employees = employees.filter(work_status__in=valid_statuses)

        
        employees = employees.exclude(EmployeeCode__isnull=True).exclude(EmployeeCode__exact='')

       
        employees = employees.filter(appointment_status=False)

        
        columns_order = ['work_departmentorg', 'full_name', 'EmployeeCode','work_departmentorg_id','EmpID',
                        'work_department', 'work_designation',
                        'work_date_of_joining', 'work_status']
       
        # Create DataFrame from employees values
        emp_df = pd.DataFrame(list(employees.values(
            'work_departmentorg', 'full_name', 'EmployeeCode','work_departmentorg_id','EmpID',
            'work_department', 'work_designation',
            'work_date_of_joining', 'work_status'
        )))
        
        if 'work_departmentorg' not in emp_df.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            emp_df = emp_df.sort_values(by='work_departmentorg', ascending=True) 
            
              
        missing_columns = [col for col in columns_order if col not in emp_df.columns]

        
        if missing_columns:
            print(f"Data not found for the following columns: {', '.join(missing_columns)}")
        else:
            
            emp_df = emp_df[columns_order]

        
        emp_df['appointment_status'] = 'Pending'
       
        PyHost = MasterAttribute.PyHost
        
        if not emp_df.empty:
            emp_df['View'] = emp_df.apply(
            lambda row: f"{PyHost}HumanResources/EditEmployee/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
            )
        else:
            print("The DataFrame is empty.")

    return emp_df



def fetch_full_and_final_data(report_type, report_options, org_id, selected_department, selected_designation, selected_year, selected_months):
    """
    Fetches filtered data for different full and final settlement report types.

    :param report_type: The type of report ("Full and final pending with auditors report", 
                        "Full and final pending with finance report", 
                        "Pending full and final report", 
                        "Full and final pending clearance report")
    :param org_id: The organization ID for filtering the data
    :param selected_department: The selected department for filtering (default is 'All')
    :param selected_designation: The selected designation for filtering (default is 'All')
    :return: A DataFrame containing the filtered full and final settlement data
    """
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")
    
    
    if org_id is None:
        data = Full_and_Final_Settltment.objects.filter(IsDelete=False)
    else:
        data = Full_and_Final_Settltment.objects.filter(OrganizationID=org_id, IsDelete=False)
    
    
    work_departmentorg = Subquery(OrganizationMaster.objects.filter(
        OrganizationID=OuterRef('OrganizationID'),
        IsDelete=False
    ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1])
    work_departmentorg_id = Subquery(
            OrganizationMaster.objects.filter(
                OrganizationID=OuterRef('OrganizationID'),
                IsDelete=False
            ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
        )
    emp_id_subquery = Subquery(
            EmployeePersonalDetails.objects.filter(
                EmployeeCode=OuterRef('Emp_Code'),
                IsDelete=False
            ).values('EmpID')[:1]
        )
    
    if selected_department != 'All':
        data = data.filter(Dept=selected_department)

    
    if selected_designation != 'All':
        data = data.filter(Designation=selected_designation)
    
    
    data = data.annotate(work_departmentorg=work_departmentorg, work_departmentorg_id=work_departmentorg_id,EmpID=emp_id_subquery)
    
    
    data = data.filter(DOJ__year__in=selected_year, DOJ__month__in=[months.index(month) + 1 for month in selected_months])   
    
    
    if report_type == "Full and final pending with auditors report":
        fields = [
            'work_departmentorg', 'Name', 'Emp_Code', 'Dept', 'Designation','work_departmentorg_id','EmpID', 
            'DOJ', 'Date_Of_Leaving', 'Absconding', 'Notice_Days_Served', 
            'AuditedBy', 'FinalStatus', 'PaymentStatus',
        ]
        data = data.filter(AuditedBy='Auditor', FinalStatus='Pending')

    elif report_type == "Full and final pending with finance report":
        fields = [
            'work_departmentorg', 'Name', 'Emp_Code', 'Dept', 'Designation','work_departmentorg_id','EmpID',  
            'DOJ', 'Date_Of_Leaving', 'Laid_Off', 'Confirmed', 'AuditedBy', 
            'PaymentStatus',  
        ]
        data = data.filter(AuditedBy='Finance', FinalStatus='Pending')

    elif report_type == "Pending full and final report":
        fields = [
            'work_departmentorg', 'Name', 'Emp_Code', 'Dept', 'Designation','work_departmentorg_id','EmpID',  
            'DOJ', 'Date_Of_Leaving', 'Resignation', 'Current_Salary', 
            'FinalStatus', 'PaymentStatus'
        ]
        data = data.filter(FinalStatus='Pending')

    elif report_type == "Full and final pending clearance report":
        fields = [
            'work_departmentorg', 'Name', 'Emp_Code', 'Dept', 'Designation','work_departmentorg_id','EmpID',  
            'DOJ', 'Date_Of_Leaving', 'Terminated', 'Confirmed', 
            'PaymentStatus'
        ]
        data = data.filter(PaymentStatus='Pending')
    
    
    data_df = pd.DataFrame(list(data.values(*fields)))
    
    
    if 'work_departmentorg' not in data_df.columns:
        print("Data not found for 'work_departmentorg'")
    else:
        
        data_df = data_df.sort_values(by='work_departmentorg', ascending=True)
    
   
    missing_columns = [col for col in fields if col not in data_df.columns]
    if missing_columns:
        print(f"Data not found for the following columns: {', '.join(missing_columns)}")
    else:
        
        data_df = data_df[fields]
    PyHost = MasterAttribute.PyHost
   
    if not data_df.empty:
            data_df['View'] = data_df.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}" if row['EmpID'] else None, axis=1
        )
    else:
            print("The DataFrame is empty.")
    return data_df



# New Joiners Report

# def IA_New_Joiners(report_type, report_options, org_id,
#                    selected_Division, selected_department,
#                    selected_designation, selected_year, selected_months):

#     if report_type not in report_options:
#         raise ValueError(f"Invalid report type: '{report_type}'")

#     if report_type != "IA New Joinees Report":
#         return pd.DataFrame()

#     # ----------- BASE FILTERS -----------
#     # DateObj = datetime.now(year=selected_year, month=selected_months[0], day=1)

#     filters = {
#         'IsDelete': False,
#         'LastApporvalStatus': 'Approved',
#         'ProposedDOJ__gt': date.today(),
#     }

#     # Organization filter
#     if org_id and org_id != '333333':
#         filters['AppliedFor'] = org_id

#     # ----------- QUERY DATA -----------
#     qs = (Assessment_Master.objects
#         .filter(**filters)
#         .order_by("ProposedDOJ")
#         .values(
#             "Name", "Department", "position", "Level",
#             "LOIStatus", "AppliedFor", "ProposedDOJ"
#         ))

#     df = pd.DataFrame(list(qs))

#     if df.empty:
#         return df

#     # ----------- MAP HOTEL NAMES -----------
#     org_map = {
#         o["OrganizationID"]: o["ShortDisplayLabel"]
#         for o in OrganizationMaster.objects.filter(
#             OrganizationID__in=df["AppliedFor"].unique(),
#             IsDelete=False, IsNileHotel=1, Activation_status=1
#         ).values("OrganizationID", "ShortDisplayLabel")
#     }

#     df["Hotel"] = df["AppliedFor"].map(org_map)

#     # ----------- RENAME COLUMNS -----------
#     df.rename(columns={
#         "Name": "Candidate_Name",
#         "Department": "Department",
#         "position": "Position",
#         "Level": "Level",
#         "LOIStatus": "LOI_Status",
#         "ProposedDOJ": "Proposed_DOJ"
#     }, inplace=True)

#     # ----------- COLUMN ORDER -----------
#     df = df[
#         [
#             "Hotel",
#             "Candidate_Name",
#             "Department",
#             "Position",
#             "Level",
#             "LOI_Status",
#             "Proposed_DOJ",
#             "AppliedFor"
#         ]
#     ]

#     return df


def IA_New_Joiners(report_type, report_options, org_id,
                   selected_Division, selected_department,
                   selected_designation, selected_year, selected_months):

    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'")

    if report_type != "IA New Joinees Report":
        return pd.DataFrame()
    
    print("Fetching IA New Joiners Data...")
    print(f"Organization ID: {org_id}")

    # ----------- BASE FILTERS -----------
    filters = {
        'IsDelete': False,
        'LastApporvalStatus': 'Approved',
        'ProposedDOJ__gt': date.today(),
    }

    # Organization filter
    if org_id and org_id != '333333':
        filters['AppliedFor'] = org_id

    # ----------- QUERY DATA -----------
    qs = (Assessment_Master.objects
        .filter(**filters)
        .order_by("ProposedDOJ")
        .values(
            "Name", "Department", "position", "Level",
            "LOIStatus", "AppliedFor", "ProposedDOJ"
        ))

    df = pd.DataFrame(list(qs))

    if df.empty:
        return df
    
    # Convert DOJ to datetime
    df["ProposedDOJ"] = pd.to_datetime(df["ProposedDOJ"], errors="coerce")

    # ----------- ADD FILTERS ON DATAFRAME -----------
    # Division filter
    # if selected_Division != "All":
    #     df = df[df["Department"] == selected_Division]

    # Department filter
    if selected_department != "All":
        df = df[df["Department"] == selected_department]

    # Designation filter
    if selected_designation != "All":
        df = df[df["position"] == selected_designation]

    # Year filter
    # if selected_year:
    #     df = df[df["ProposedDOJ"].dt.year.isin(selected_year)]

    # # Month filter
    # if selected_months:
    #     selected_month_numbers = [months.index(m) + 1 for m in selected_months]
    #     df = df[df["ProposedDOJ"].dt.month.isin(selected_month_numbers)]

    if df.empty:
        return df

    # ----------- MAP HOTEL NAMES -----------
    org_map = {
        o["OrganizationID"]: o["ShortDisplayLabel"]
        for o in OrganizationMaster.objects.filter(
            OrganizationID__in=df["AppliedFor"].unique(),
            IsDelete=False, IsNileHotel=1, Activation_status=1
        ).values("OrganizationID", "ShortDisplayLabel")
    }

    df["Hotel"] = df["AppliedFor"].map(org_map)

    # ----------- RENAME COLUMNS -----------
    df.rename(columns={
        "Name": "Candidate_Name",
        "Department": "Department",
        "position": "Position",
        "Level": "Level",
        "LOIStatus": "LOI_Status",
        "ProposedDOJ": "Proposed_DOJ"
    }, inplace=True)

    # ----------- COLUMN ORDER -----------
    df = df[
        [
            "Hotel",
            "Candidate_Name",
            "Department",
            "Position",
            "Level",
            "LOI_Status",
            "Proposed_DOJ",
            # "AppliedFor"
        ]
    ]

    return df




if selected_report == "Employees on Resignation":
    resignation_reasons = EmpResigantionModel.objects.filter(OrganizationID=org_id, IsDelete=False).values_list('Res_Reason', flat=True).distinct()
    selected_resignation_reason = st.sidebar.selectbox("Choose a resignation reason", ['All'] + list(resignation_reasons))

    df_resignation = fetch_filtered_data(
        "Employees on Resignation", report_options, org_id, selected_Division, selected_department, 
        selected_designation, selected_year, selected_months, selected_resignation_reason
    )


elif selected_report == "Employees on Termination":
    df_termination = fetch_filtered_data(
        "Employees on Termination", report_options, org_id, selected_Division. selected_department, 
        selected_designation, selected_year, selected_months
    )


elif selected_report == "New Joinees Report":
    df_new_joinees = fetch_new_joinees_data( "New Joinees Report", org_id, selected_Division, selected_department,
        selected_designation, selected_year, selected_months, report_options)

elif selected_report == "Emergency Contact Report":
    df_new_Emergency_data = fetch_new_Emergency_data(
        "Emergency Contact Report", report_options, org_id, selected_Division, selected_department, 
        selected_designation, selected_year, selected_months
    )

elif selected_report == "Blood Group Report":
    df_blood_data = fetch_blood_data("Blood Group Report",report_options, org_id, selected_Division, selected_department, selected_designation,selected_year, selected_months,)

elif selected_report == "IA New Joinees Report":
    df_IA_New_Joiners = IA_New_Joiners("IA New Joinees Report",report_options, org_id, selected_Division, selected_department, selected_designation,selected_year, selected_months,)

elif selected_report == "Absconding Employees Report":
    df_Absconding_data = fetch_absconding_data("Absconding Employees Report",report_options, selected_Division, org_id,selected_department, selected_designation,selected_year, selected_months,)



elif selected_report == "Terminated Employees":
    df_TerminateEmployees_data = fetch_TerminateEmployees_data("Terminated Employees",report_options, selected_Division, org_id,selected_department, selected_designation,selected_year, selected_months,)


elif selected_report == "Upcoming Birthday's report":
    df_Birthday_data = fetch_Birthdays_data("Upcoming Birthday's report",report_options, selected_Division, org_id,selected_year, selected_months,selected_department, selected_designation)

elif selected_report == "Actual Salary OnRoll Report":
    df_headsalary_data = fetch_Acutalcounthr("Actual Salary OnRoll Report",report_options, selected_Division, org_id,selected_year, selected_months,selected_department, selected_designation)


elif selected_report == "Actual Head Count OnRoll Report":
    df_headHeadCount_data = fetch_AcutalHeadCounthr("Actual Head Count OnRoll Report",report_options, selected_Division, org_id,selected_department, selected_designation)



elif selected_report == "Actual Contract Report":
    df_ActualContract_data = fetch_ActualContracthr("Actual Contract Report",report_options, selected_Division, org_id,selected_department, selected_designation)

 

elif selected_report == "Actual Shared Services":
    df_ActualSharedServices_data = fetch_ActualSharedServiceshr(
        "Actual Shared Services",
        report_options,
        selected_Division,
        org_id,
        selected_department,
        selected_designation
    )

elif selected_report == "Actual Meal Cost":
    df_ActualMealCost_data = fetch_ActualMealCosthr(
        "Actual Meal Cost",
        report_options,
        selected_Division,
        org_id,
        selected_department,
        selected_designation
    )

elif selected_report == "Actual Insurance Cost":
    df_ActualInsuranceCost_data = fetch_ActualInsuranceCosthr(
        "Actual Insurance Cost",
        report_options,
        org_id,
        selected_department,
        selected_designation
    )



elif selected_report == "Budget On Roll Report":
    df_BudgetOnRoll_data = fetch_BudgetOnRollhr(
        "Budget On Roll Report",
        report_options,
        selected_Division,
        org_id,
        selected_department,
        selected_designation
    )


elif selected_report == "Budget Insurance Cost Report":
    df_BudgetInsuranceCost_data = fetch_BudgetInsuranceCosthr(
        "Budget Insurance Cost Report",
        report_options,
        selected_Division,
        org_id,
        selected_department,
        selected_designation
    )


elif selected_report == "Budget Contract Report":
    df_BudgetContract_data = fetch_BudgetContracthr(
        "Budget Contract Report",
        report_options,
        selected_Division,
        org_id,
        selected_department,
        selected_designation
    )


elif selected_report == "Budget Meal Cost Report":
    df_BudgetMealCost_data = fetch_BudgetMealCosthr(
        "Budget Meal Cost Report",
        report_options,
        selected_Division,
        org_id,
        selected_department,
        selected_designation
    )


elif selected_report == "Budget Shared Services Report":
    df_BudgetSharedServices_data = fetch_BudgetSharedServiceshr(
        "Budget Shared Services Report",
        report_options,
        selected_Division,
        org_id,
        selected_department,
        selected_designation
    )


elif selected_report == "Employees Serving Notice Period":
    df_Notice_data = fetch_Notice_data("Employees Serving Notice Period",report_options, selected_Division, org_id,selected_department, selected_designation,selected_year, selected_months)       

elif selected_report == "Exit Interview Report":
    df_exit_interview_data = fetch_exit_interview_data("Exit Interview Report",report_options, selected_Division, org_id,selected_department, selected_designation)       

   


def format_date(date_value):
    return date_value.strftime("%d %b %Y") if date_value else None



# Assuming df_resignation, df_termination, and df_new_joinees are already defined



if 'df_resignation' in locals() and not df_resignation.empty:
    df_resignation['DOJ'] = df_resignation['DOJ'].apply(format_date)
    df_resignation['Date_Of_res'] = df_resignation['Date_Of_res'].apply(format_date)
    df_resignation['LastWorkingDays'] = df_resignation['LastWorkingDays'].apply(format_date)
    df_resignation = df_resignation.rename(columns={
        'Name': 'Name',
        'Emp_Code': 'Emp Code',
        'work_departmentorg':'Hotel Name',
        'Divi': 'Division',
        'Dept': 'Department',
        'Designation': 'Designation',
        'DOJ': 'Date of Joining',
        'Date_Of_res': 'Date of Resignation',
        'Res_Reason': 'Reason',
        'TypeofRes': 'Type',
        'LastWorkingDays': 'Last Working',
    })


if 'df_termination' in locals() and not df_termination.empty:
    df_termination['DOJ'] = df_termination['DOJ'].apply(format_date)
    df_termination = df_termination.rename(columns={
        'Name': 'Name',
        'Emp_Code': 'Emp Code',
        'work_departmentorg':'Hotel Name',
        'Divi': 'Division',
        'Dept': 'Department',
        'Designation': 'Designation',
        'DOJ': 'DOJ',
        'Remarks': 'Remarks',
        'LastWarningLatter': 'Last Warning',
    })


if 'df_new_joinees' in locals() and not df_new_joinees.empty:
    df_new_joinees['work_date_of_joining'] = df_new_joinees['work_date_of_joining'].apply(format_date)
    df_new_joinees = df_new_joinees.rename(columns={
        'work_departmentorg':'Hotel Name',
        'full_name': 'Name',
        'EmployeeCode': 'Emp Code',
        'work_division': 'Division',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'work_date_of_joining': 'Date of Joining',
        'work_status': 'Status',
       
    })


if 'df_new_Emergency_data' in locals() and not df_new_Emergency_data.empty:
    df_new_Emergency_data['work_date_of_joining'] = df_new_Emergency_data['work_date_of_joining'].apply(format_date)
    df_new_Emergency_data = df_new_Emergency_data.rename(columns={
        'full_name': 'Name',
        'work_departmentorg':'Hotel Name',
        'EmployeeCode': 'Emp Code',
        'work_division': 'Division',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'work_date_of_joining': 'Date of Joining',
        'work_status':'Status',
        'emergency_first_name':'Emergency Name',
        'emergency_relation':'Emergency Relation',
        'emergency_contact_1':'Emergency Contact 1', 'emergency_contact_2':'Emergency Contact 2',
           
    })

if 'df_blood_data' in locals() and not df_blood_data.empty:
    df_blood_data['work_date_of_joining'] = df_blood_data['work_date_of_joining'].apply(format_date)
    df_blood_data = df_blood_data.rename(columns={
        'full_name': 'Name',
        'work_departmentorg':'Hotel Name',
        'EmployeeCode': 'Emp Code',
        'work_division': 'Division',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'work_ReportingToDesignation':'Reporting To Designation',
        'work_date_of_joining': 'Date of Joining',
        'work_status':'Status',
        'Blood_Group':'Blood Group',
           
    })

if 'df_IA_New_Joiners' in locals() and not df_IA_New_Joiners.empty:
    df_IA_New_Joiners['Proposed_DOJ'] = df_IA_New_Joiners['Proposed_DOJ'].apply(format_date)

    df_IA_New_Joiners = df_IA_New_Joiners.rename(columns={
        "Hotel": "Hotel Name",
        "Candidate_Name": "Candidate Name",
        "Department": "Department",
        "Position": "Position",
        "Level": "Level",
        "LOI_Status": "LOI Status",
        "Proposed_DOJ": "Proposed DOJ",
        # "AppliedFor": "Hotel OID"
    })


if 'df_Absconding_data' in locals() and not df_Absconding_data.empty:
    df_Absconding_data['DOJ'] = df_Absconding_data['DOJ'].apply(format_date)
    df_Absconding_data['Date_Of_Absconding'] = df_Absconding_data['Date_Of_Absconding'].apply(format_date)
    df_Absconding_data = df_Absconding_data.rename(columns={
        'Emp_Code': 'Emp Code',
        'work_departmentorg':'Hotel Name',
        'Name': 'Name',
        'Dept': 'Department',
        'Divi': 'Division',
        'Designation': 'Designation',
        'DOJ': 'Date of Joining',
        'Date_Of_Absconding':'Date Of Absconding'
           
    })

if 'df_TerminateEmployees_data' in locals() and not df_TerminateEmployees_data.empty:
  
    df_TerminateEmployees_data['Date_Of_Termination'] = df_TerminateEmployees_data['Date_Of_Termination'].apply(format_date)
    df_TerminateEmployees_data = df_TerminateEmployees_data.rename(columns={
        'work_departmentorg':'Hotel Name',
        'Name': 'Name',
        'Dept': 'Department',
        'Divi': 'Division',
        'Designation': 'Designation',
        'DOJ': 'Date of Joining',
        'Date_Of_Termination':'Date Of Termination'
           
    })
if 'df_Birthday_data' in locals() and not df_Birthday_data.empty:
    df_Birthday_data['DateofBirth'] = df_Birthday_data['DateofBirth'].apply(format_date)
    df_Birthday_data = df_Birthday_data.rename(columns={
        'full_name': 'Name',
        'work_departmentorg':'Hotel Name',
        'EmployeeCode': 'Emp Code',
        'work_division': 'Division',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'DateofBirth': 'Date of Birth',
        'work_status':'Status',
    })


if 'df_headsalary_data' in locals() and not df_headsalary_data.empty:
    
    df_headsalary_data = df_headsalary_data.rename(columns={
        'work_departmentorg':'Hotel Name',
        'work_Salary':'Salary',
        'work_division': 'Division',
        'work_department': 'Department',
        'work_designation': 'Designation',
    })


if 'df_headHeadCount_data' in locals() and not df_headHeadCount_data.empty:
    
    df_headHeadCount_data = df_headHeadCount_data.rename(columns={
        
        'work_departmentorg':'Hotel Name',
        'head_count':'Head Count',
        'work_division': 'Division',
        'work_department': 'Department',
        'work_designation': 'Designation',
        
    })



if 'df_ActualContract_data' in locals() and not df_ActualContract_data.empty:
    
    df_ActualContract_data = df_ActualContract_data.rename(columns={
        'work_departmentorg':'Hotel Name',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'work_division':'Division',  # Division
        'avg_salary':'Avg Salary',  # Average Salary
        'head_count':'Head  Count',
        'total_ctc':'Total CTC',
    })

if 'df_ActualSharedServices_data' in locals() and not df_ActualSharedServices_data.empty:
    # Rename columns
    df_ActualSharedServices_data = df_ActualSharedServices_data.rename(columns={
        'work_departmentorg': 'Hotel Name',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'work_division': 'Division',
        'avg_salary': 'Avg Salary',
        'head_count': 'Head Count',
        'total_ctc': 'Total CTC',
    })



if 'df_BudgetSharedServices_data' in locals() and not df_BudgetSharedServices_data.empty:
    # Rename columns
    df_BudgetSharedServices_data = df_BudgetSharedServices_data.rename(columns={
        'work_departmentorg': 'Hotel Name',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'work_division': 'Division',
        'avg_salary': 'Avg Salary',
        'head_count': 'Head Count',
        'total_ctc': 'Total CTC',
    })

if 'df_ActualMealCost_data' in locals() and not df_ActualMealCost_data.empty:
    # Rename columns
    df_ActualMealCost_data = df_ActualMealCost_data.rename(columns={
        'work_departmentorg': 'Hotel Name',
        
        'cafeteriamealcost': 'Cafeteria Meal Cost',
    })


if 'df_BudgetMealCost_data' in locals() and not df_BudgetMealCost_data.empty:
    # Rename columns
    df_BudgetMealCost_data = df_BudgetMealCost_data.rename(columns={
        'work_departmentorg': 'Hotel Name',
        
        'cafeteriamealcost': 'Cafeteria Meal Cost',
    })



if 'df_ActualInsuranceCost_data' in locals() and not df_ActualInsuranceCost_data.empty:
    # Rename columns
    df_ActualInsuranceCost_data = df_ActualInsuranceCost_data.rename(columns={
        'work_departmentorg': 'Hotel Name',
        'EmployeeInsurancecost':'Employee Insurance Cost'
        
    })



if 'df_BudgetInsuranceCost_data' in locals() and not df_BudgetInsuranceCost_data.empty:
    # Rename columns
    df_BudgetInsuranceCost_data = df_BudgetInsuranceCost_data.rename(columns={
        'work_departmentorg': 'Hotel Name',
        'EmployeeInsurancecost':'Employee Insurance Cost'
        
    })


if 'df_BudgetOnRoll_data' in locals() and not df_BudgetOnRoll_data.empty:
    # Rename columns
    df_BudgetOnRoll_data = df_BudgetOnRoll_data.rename(columns={
         'work_departmentorg': 'Hotel Name',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'work_division': 'Division',
        'avg_salary': 'Avg Salary',
        'head_count': 'Head Count',
        'total_ctc': 'Total CTC',
    })


if 'df_BudgetContract_data' in locals() and not df_BudgetContract_data.empty:
    # Rename columns
    df_BudgetContract_data = df_BudgetContract_data.rename(columns={
         'work_departmentorg': 'Hotel Name',
        'work_department': 'Department',
        'work_designation': 'Designation',
        'work_division': 'Division',
        'avg_salary': 'Avg Salary',
        'head_count': 'Head Count',
        'total_ctc': 'Total CTC',
    })





if 'df_Notice_data' in locals() and not df_Notice_data.empty:
    df_Notice_data['DOJ'] = df_Notice_data['DOJ'].apply(format_date)
    df_Notice_data['Date_Of_res'] = df_Notice_data['Date_Of_res'].apply(format_date)
    df_Notice_data = df_Notice_data.rename(columns={
        'Name': 'Name',
        'Emp_Code': 'Employee Code',
         'work_departmentorg': 'Hotel Name',
        'Dept': 'Department',
        'Designation': 'Designation',
        'DOJ': 'Date of Joining',
        'Date_Of_res' : 'Date of Res', 
        'NoticePeriod':'NoticePeriod'
    })

import pandas as pd

def format_date(date):
    if pd.isna(date):  # Check if the date is NaT or NaN
        return date
    # Format the date as '23 Dec 2024'
    return date.strftime('%d %b %Y')

if 'df_exit_interview_data' in locals() and not df_exit_interview_data.empty:
    # Convert 'DateofLeaving' to datetime if it is not already in datetime format
    df_exit_interview_data['DateofLeaving'] = pd.to_datetime(df_exit_interview_data['DateofLeaving'], errors='coerce')

    # Apply the date formatting function to 'DateofLeaving'
    df_exit_interview_data['DateofLeaving'] = df_exit_interview_data['DateofLeaving'].apply(format_date)

    # Rename columns
    df_exit_interview_data = df_exit_interview_data.rename(columns={
        'Employee_Code': 'Emp Code',
        'EmpName': 'Name',
        'work_departmentorg': 'Hotel Name',
        'Job_Title': 'Designation',
        'Department': 'Department',
        'DateofJoining': 'Date of Joining',
        'DateofLeaving': 'Date of Leaving',
        'NoticePeriod': 'NoticePeriod',
        'Resign': 'Resign',
        'Termination': 'Termination',
    })

 

def convert_df_to_excel(df):
    """Convert a DataFrame to an Excel file and return as a bytes object."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')
    output.seek(0)
    return output.read()


from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import textwrap

def wrap_text_for_table(data, column_widths):
    wrapped_data = []
    
    
    if len(column_widths) != len(data[0]):
        raise ValueError("The number of column widths must match the number of columns in the data.")
    
    for row in data:
        wrapped_row = []
        
        for i, cell in enumerate(row):
            
            if isinstance(cell, str):
                if(column_widths[i]<(len(cell)*5)+12):
                    w=int(column_widths[i]/8)
                    if w<1:
                        w=1
                    # wrapped_text = textwrap.fill(cell, width=int(column_widths[i]/4))  # Use column_widths dynamically
                    wrapped_text = textwrap.fill(cell, width=w)  # Use column_widths dynamically
                    wrapped_row.append(wrapped_text)
                else:
                    wrapped_row.append(cell)
            else:
                # If it's not a string, just append it as-is
                wrapped_row.append(cell)
        
        wrapped_data.append(wrapped_row)
    
    return wrapped_data

def create_pdf_report(data_frame, report_title, organization_name):
    buffer = BytesIO()
    
    
    left_margin = 0
    right_margin = 0
    top_margin = 0
    bottom_margin = 0
    
    
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            leftMargin=left_margin, rightMargin=right_margin,
                            topMargin=top_margin, bottomMargin=bottom_margin)

    elements = []
    
    # Title section
    title_text = f"{report_title} - {organization_name}"
    title = [[title_text]]
   

    # Example usage
    
    title_table = Table(title, colWidths=[700 - left_margin - right_margin])
    title_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9)
    ]))
    elements.append(title_table)
   
    # Prepare the data for the table
    data = [data_frame.columns.tolist()] + data_frame.values.tolist()

    # Column width: Calculate based on the maximum text length
    column_widths = [max(len(str(val)) for val in data_frame[col].values.tolist()) * 8 for col in data_frame.columns]

    # Ensure that total width doesn't exceed page width
    max_width = 700 - left_margin - right_margin
    total_width = sum(column_widths)
    if total_width > max_width:
        # Scale down column widths proportionally
        scale_factor = max_width / total_width
        column_widths = [width * scale_factor for width in column_widths]
    wrapped_data = wrap_text_for_table(data,column_widths)
    # Create the table with the data
    col_widths = [80] * len(data_frame.columns)
    table = Table(wrapped_data,   colWidths=column_widths)

    # Apply the table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Grey background for header row
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # White text for header
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all text to center
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header
        ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for header
        ('FONTSIZE', (0, 1), (-1, -1), 9),  # Font size for body
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Padding for header row
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # White background for data rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines between cells
        ('WORDSPACE', (0, 0), (-1, -1), 1),  # Adjust word spacing for readability
        ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Add padding inside cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Add padding inside cells
        ('TOPPADDING', (0, 0), (-1, -1), 5),  # Add padding inside cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Add padding inside cells
        ('WORDWRAP', (0, 0), (-1, -1), True)  # Enable word wrapping for all cells
    ]))

    # Append the table to the document's elements
    elements.append(table)

    # Build the document
    doc.build(elements)
    
    # Rewind the buffer and return its content
    buffer.seek(0)
    return buffer.getvalue()

def create_pdf_report_OLd(data_frame, report_title, organization_name):
    buffer = io.BytesIO()
    
    left_margin = 20
    right_margin = 20
    top_margin = 10
    bottom_margin = 10
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            leftMargin=left_margin, rightMargin=right_margin,
                            topMargin=top_margin, bottomMargin=bottom_margin)

    elements = []
    
    title_text = f"{report_title} - {organization_name}"
    title = [[title_text]]
    title_table = Table(title, colWidths=[700 - left_margin - right_margin])  
    title_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))
    elements.append(title_table)

    data = [data_frame.columns.tolist()] + data_frame.values.tolist()

    column_widths = {
        # 'Name': 120,
        # 'Emp_Code': 40,
        # 'Dept': 150,
        # 'Designation': 150,
        # 'DOJ': 90,
        # 'Remarks': 70,
        # 'LastWarningLatter': 100
    }
    
   
    col_widths = [column_widths.get(col, 100) for col in data_frame.columns]

    
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10), 
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

st.markdown(
    """
    <style>
    .stMainBlockContainer{
        max-width: 100%;
    }
    .stDataFrame {
        width: 100%;
        max-width: 100%;
    }
    .dataframe {
        width: 100% !important;  /* Set table width to 100% */
    }
 
    </style>
    """,
    unsafe_allow_html=True
)

if selected_report == "Employees on Resignation":
    st.header("Employees on Resignation")
    if 'df_resignation' in locals() and not df_resignation.empty:
        df_display = df_resignation.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        excel_data = convert_df_to_excel(df_resignation)
        pdf_data = create_pdf_report(df_resignation, "Employees on Resignation", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='resignation_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='resignation_report.pdf', mime='application/pdf')
    else:
        st.write("No resignation data available.")

elif selected_report == "Employees on Termination":
    st.header("Employees on Termination")
    if 'df_termination' in locals() and not df_termination.empty:
        df_display = df_termination.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        

        excel_data = convert_df_to_excel(df_termination)
        pdf_data = create_pdf_report(df_termination, "Employees on Termination", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='termination_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='termination_report.pdf', mime='application/pdf')
    else:
        st.write("No termination data available.")

if selected_report == "New Joinees Report":
    st.header("New Joinees Report")
    
    # Check if the DataFrame exists and is not empty
    if 'df_new_joinees' in locals() and not df_new_joinees.empty:
        # Drop unnecessary columns and reset index
        df_display = df_new_joinees.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})

        # Convert the DataFrame to Excel and PDF
        excel_data = convert_df_to_excel(df_new_joinees)
        pdf_data = create_pdf_report(df_new_joinees, "New Joinees Report", selected_org)

        # Display download buttons for Excel and PDF
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥 Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥 Download PDF", data=pdf_data, file_name='new_joinees_report.pdf', mime='application/pdf')
    
    else:
        st.write("No new joinees data available.")

if selected_report == "Emergency Contact Report":
    st.header("Emergency Contact Report")
    if 'df_new_Emergency_data' in locals() and not df_new_Emergency_data.empty:
       
        df_display = df_new_Emergency_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        excel_data = convert_df_to_excel(df_new_Emergency_data)
        pdf_data = create_pdf_report(df_new_Emergency_data, "Emergency Contact Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='new_joinees_report.pdf', mime='application/pdf')
    else:
        st.write("No new joinees data available.")


if selected_report == "Blood Group Report":
    st.header("Blood Group Report")
    if 'df_blood_data' in locals() and not df_blood_data.empty:
        df_display = df_blood_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        
        
        excel_data = convert_df_to_excel(df_blood_data)
        pdf_data = create_pdf_report(df_blood_data, "Blood Group Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='new_joinees_report.pdf', mime='application/pdf')
    else:
        st.write("No new joinees data available.")     


if selected_report == "IA New Joinees Report":
    st.header("IA New Joinees Report")

    if 'df_IA_New_Joiners' in locals() and not df_IA_New_Joiners.empty:

        df_display = df_IA_New_Joiners.copy()
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1

        # Show dataframe
        st.dataframe(df_display, width=1400)

        # ----- EXPORT -----
        excel_data = convert_df_to_excel(df_display)
        pdf_data = create_pdf_report(df_display, "IA New Joinees Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name='ia_new_joinees_report.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        with col2:
            st.download_button(
                label="📥 Download PDF",
                data=pdf_data,
                file_name='ia_new_joinees_report.pdf',
                mime='application/pdf'
            )

    else:
        st.write("No new joinees data available.")
  

if selected_report == "Absconding Employees Report":
    st.header("Absconding Employees Report")
    if 'df_Absconding_data' in locals() and not df_Absconding_data.empty:
        
        df_Absconding_data = df_Absconding_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_Absconding_data.reset_index(drop=True, inplace=True)
        df_Absconding_data.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_Absconding_data, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        
        excel_data = convert_df_to_excel(df_Absconding_data)
        pdf_data = create_pdf_report(df_Absconding_data, "Absconding Employees Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='new_joinees_report.pdf', mime='application/pdf')
    else:
        st.write("No new joinees data available.")                   


if selected_report == "Terminated Employees":
    st.header("Terminated Employees")
    if 'df_TerminateEmployees_data' in locals() and not df_TerminateEmployees_data.empty:
        
        df_TerminateEmployees_data.reset_index(drop=True, inplace=True)
        df_TerminateEmployees_data.index += 1
       
        st.dataframe(df_TerminateEmployees_data, width=1400)
        
        excel_data = convert_df_to_excel(df_TerminateEmployees_data)
        pdf_data = create_pdf_report(df_TerminateEmployees_data, "Terminated Employees", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='df_TerminateEmployees_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_TerminateEmployees_data.pdf', mime='application/pdf')
    else:
        st.write("No new joinees data available.")    

if selected_report == "Upcoming Birthday's report":
    st.header("Upcoming Birthday's Report")
    if 'df_Birthday_data' in locals() and not df_Birthday_data.empty:
        df_display = df_Birthday_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        
        
        excel_data = convert_df_to_excel(df_Birthday_data)
        pdf_data = create_pdf_report(df_Birthday_data, "Upcoming Birthday's report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='new_joinees_report.pdf', mime='application/pdf')
    else:
        st.write("No new joinees data available.")



if selected_report == "Actual Salary OnRoll Report":
    st.header("Actual Salary OnRoll Report")
    if 'df_headsalary_data' in locals() and not df_headsalary_data.empty:
        df_headsalary_data.reset_index(drop=True, inplace=True)
        df_headsalary_data.index += 1
       
        st.dataframe(df_headsalary_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_headsalary_data)
        pdf_data = create_pdf_report(df_headsalary_data, "Actual Salary OnRoll Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_headsalary_data.pdf', mime='application/pdf')
    else:
        st.write("No Actual Salary OnRoll Report data available.")




if selected_report == "Actual Head Count OnRoll Report":
    st.header("Actual Head Count OnRoll Report")
    if 'df_headHeadCount_data' in locals() and not df_headHeadCount_data.empty:
        df_headHeadCount_data.reset_index(drop=True, inplace=True)
        df_headHeadCount_data.index += 1
       
        st.dataframe(df_headHeadCount_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_headHeadCount_data)
        pdf_data = create_pdf_report(df_headHeadCount_data, "Actual Head Count OnRoll Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_headHeadCount_data.pdf', mime='application/pdf')
    else:
        st.write("No Actual Head Count OnRoll Report data available.")



if selected_report == "Actual Contract Report":
    st.header("Actual Contract Report")
    if 'df_ActualContract_data' in locals() and not df_ActualContract_data.empty:
        df_ActualContract_data.reset_index(drop=True, inplace=True)
        df_ActualContract_data.index += 1
       
        st.dataframe(df_ActualContract_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_ActualContract_data)
        pdf_data = create_pdf_report(df_ActualContract_data, "Actual Contract Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_ActualContract_data.pdf', mime='application/pdf')
    else:
        st.write("No Actual Contract Report data available.")




if selected_report == "Actual Meal Cost":
    st.header("Actual Meal Cost Report")
    if 'df_ActualMealCost_data' in locals() and not df_ActualMealCost_data.empty:
        df_ActualMealCost_data.reset_index(drop=True, inplace=True)
        df_ActualMealCost_data.index += 1
       
        st.dataframe(df_ActualMealCost_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_ActualMealCost_data)
        pdf_data = create_pdf_report(df_ActualMealCost_data, "Actual Salary OnRoll Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='df_ActualMealCost_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_ActualMealCost_data.pdf', mime='application/pdf')
    else:
        st.write("No Actual Meal Cost Report Report data available.")

if selected_report == "Actual Insurance Cost":
    st.header("Actual Insurance Cost Report")
    if 'df_ActualInsuranceCost_data' in locals() and not df_ActualInsuranceCost_data.empty:
        df_ActualInsuranceCost_data.reset_index(drop=True, inplace=True)
        df_ActualInsuranceCost_data.index += 1
       
        st.dataframe(df_ActualInsuranceCost_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_ActualInsuranceCost_data)
        pdf_data = create_pdf_report(df_ActualInsuranceCost_data, "Actual Insurance Cost", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='df_ActualInsuranceCost_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_ActualInsuranceCost_data.pdf', mime='application/pdf')
    else:
        st.write("No Actual Meal Cost Report Report data available.")




if selected_report == "Budget On Roll Report":
    st.header("Budget On Roll Report")
    if 'df_BudgetOnRoll_data' in locals() and not df_BudgetOnRoll_data.empty:
        df_BudgetOnRoll_data.reset_index(drop=True, inplace=True)
        df_BudgetOnRoll_data.index += 1
       
        st.dataframe(df_BudgetOnRoll_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_BudgetOnRoll_data)
        pdf_data = create_pdf_report(df_BudgetOnRoll_data, "Budget On Roll Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='df_BudgetOnRoll_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_BudgetOnRoll_data.pdf', mime='application/pdf')
    else:
        st.write("No Budget On Roll Report data available.")

if selected_report == "Budget Contract Report":
    st.header("Budget Contract Report")
    if 'df_BudgetContract_data' in locals() and not df_BudgetContract_data.empty:
        df_BudgetContract_data.reset_index(drop=True, inplace=True)
        df_BudgetContract_data.index += 1
       
        st.dataframe(df_BudgetContract_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_BudgetContract_data)
        pdf_data = create_pdf_report(df_BudgetContract_data, "Budget Contract Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='df_BudgetContract_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_BudgetContract_data.pdf', mime='application/pdf')
    else:
        st.write("No Budget Contract Report data available.")



if selected_report == "Budget Shared Services Report":
    st.header("Budget Shared Services Report")
    if 'df_BudgetSharedServices_data' in locals() and not df_BudgetSharedServices_data.empty:
        df_BudgetSharedServices_data.reset_index(drop=True, inplace=True)
        df_BudgetSharedServices_data.index += 1
       
        st.dataframe(df_BudgetSharedServices_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_BudgetSharedServices_data)
        pdf_data = create_pdf_report(df_BudgetSharedServices_data, "Budget Contract Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='df_BudgetSharedServices_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_BudgetSharedServices_data.pdf', mime='application/pdf')
    else:
        st.write("No Budget Shared Services Report data available.")



if selected_report == "Budget Insurance Cost Report":
    st.header("Budget Insurance Cost Report")
    if 'df_BudgetInsuranceCost_data' in locals() and not df_BudgetInsuranceCost_data.empty:
        df_BudgetInsuranceCost_data.reset_index(drop=True, inplace=True)
        df_BudgetInsuranceCost_data.index += 1
       
        st.dataframe(df_BudgetInsuranceCost_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_BudgetInsuranceCost_data)
        pdf_data = create_pdf_report(df_BudgetInsuranceCost_data, "Budget Insurance Cost Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='df_BudgetInsuranceCost_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_BudgetInsuranceCost_data.pdf', mime='application/pdf')
    else:
        st.write("No Budget Insurance Cost Report data available.")


if selected_report == "Budget Meal Cost Report":
    st.header("Budget Meal Cost Report")
    if 'df_BudgetMealCost_data' in locals() and not df_BudgetMealCost_data.empty:
        df_BudgetMealCost_data.reset_index(drop=True, inplace=True)
        df_BudgetMealCost_data.index += 1
       
        st.dataframe(df_BudgetMealCost_data, width=1400)
        
        
        excel_data = convert_df_to_excel(df_BudgetMealCost_data)
        pdf_data = create_pdf_report(df_BudgetMealCost_data, "Budget Meal Cost Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='df_BudgetMealCost_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='df_BudgetMealCost_data.pdf', mime='application/pdf')
    else:
        st.write("No Budget Meal Cost Report data available.")






if selected_report == "Actual Shared Services":
    st.header("Actual Shared Services Report")
    
    if 'df_ActualSharedServices_data' in locals() and not df_ActualSharedServices_data.empty:
        # Reset index for better display
        df_ActualSharedServices_data.reset_index(drop=True, inplace=True)
        df_ActualSharedServices_data.index += 1

        # Display data
        st.dataframe(df_ActualSharedServices_data, width=1400)

        # Generate files for download
        excel_data = convert_df_to_excel(df_ActualSharedServices_data)
        pdf_data = create_pdf_report(df_ActualSharedServices_data, "Actual Shared Services", selected_org)

        # Sidebar download buttons
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(
                label="📥Download Excel",
                data=excel_data,
                file_name='actual_shared_services_report.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        with col2:
            st.download_button(
                label="📥Download PDF",
                data=pdf_data,
                file_name='actual_shared_services_report.pdf',
                mime='application/pdf'
            )
    else:
        st.write("No Actual Shared Services data available.")

if selected_report == "Employees on Probation":
    st.header("Employees on Probation")
    
    # Fetch probation data
    df_probation_data = fetch_probation_data(
        selected_report, report_options, org_id,
        selected_department, selected_designation,
        selected_year, selected_months
    )

    # Check if the data is empty
    if df_probation_data.empty:
        st.write("No data available for the selected filters.")
    else:
        # Export options (Excel and PDF)
        excel_data = convert_df_to_excel(df_probation_data)
        
        # Check if the data is empty before creating the PDF
        if df_probation_data.empty:
            st.write("No data available to generate PDF.")
        else:
            pdf_data = create_pdf_report(df_probation_data, "Employees on Probation", org_id)

            # Display download buttons in two columns
            col1, col2 = st.sidebar.columns(2)
            with col1:
               st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            with col2:
               st.download_button(label="📥Download PDF", data=pdf_data, file_name='new_joinees_report.pdf', mime='application/pdf')



if selected_report == "Employees Serving Notice Period":
    st.header("Employees Serving Notice Period")
    if 'df_Notice_data' in locals() and not df_Notice_data.empty:
        df_Notice_data = df_Notice_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_Notice_data.reset_index(drop=True, inplace=True)
        df_Notice_data.index += 1
        
       
        st.dataframe(df_Notice_data, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        
        
        excel_data = convert_df_to_excel(df_Notice_data)
        pdf_data = create_pdf_report(df_Notice_data, "Employees Serving Notice Period", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='new_joinees_report.pdf', mime='application/pdf')
    else:
        st.write("No new joinees data available.") 


if selected_report == "Exit Interview Report":
    st.header("Exit Interview Report")
    if 'df_exit_interview_data' in locals() and not df_exit_interview_data.empty:
        df_exit_interview_data = df_exit_interview_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_exit_interview_data.reset_index(drop=True, inplace=True)
        df_exit_interview_data.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_exit_interview_data, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        
        
        excel_data = convert_df_to_excel(df_exit_interview_data)
        pdf_data = create_pdf_report(df_exit_interview_data, "Exit Interview Report", selected_org)

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='new_joinees_report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='new_joinees_report.pdf', mime='application/pdf')
    else:
        st.write("No new joinees data available.")  


if selected_report == "Leave balance report":
    df_leave_balance_data = fetch_leave_balance_report(
        "Leave balance report", report_options, org_id, selected_department, selected_designation
    )
    st.header("Leave Balance Report")

    if not df_leave_balance_data.empty:
        # Format the date and rename columns for display
        df_leave_balance_data['work_date_of_joining'] = df_leave_balance_data['work_date_of_joining'].apply(format_date)
        df_leave_balance_data = df_leave_balance_data.rename(columns={
            'full_name': 'Name',
            'EmployeeCode': 'Emp Code',
            'work_department': 'Department',
            'work_designation': 'Designation',
            'work_date_of_joining': 'Date of Joining',
            'work_departmentorg': 'Hotel Name',
        })

        # Drop unnecessary columns and reset the index
       
        df_leave_balance_data.reset_index(drop=True, inplace=True)
        df_leave_balance_data.index += 1

        # Add hyperlinks for the "View" column
        PyHost = MasterAttribute.PyHost  # Replace with actual PyHost if needed
        df_leave_balance_data['View'] = df_leave_balance_data.apply(
            lambda row: f"{PyHost}HumanResources/PersonalDetails/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}"
            if row['Emp Code'] else None,
            axis=1
        )
        df_leave_balance_data = df_leave_balance_data.drop(columns=['EmpID', 'work_departmentorg_id'])
       
        st.data_editor(
            df_leave_balance_data,
            use_container_width=True,
            column_config={
                "View": st.column_config.LinkColumn(label="View", display_text="View Details")
            },
            hide_index=False  
        )
        
        excel_data = convert_df_to_excel(df_leave_balance_data)
        pdf_data = create_pdf_report(df_leave_balance_data, "Leave Balance Report", selected_org)

       
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(
                label="📥Download Excel",
                data=excel_data,
                file_name='leave_balance_report.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        with col2:
            st.download_button(
                label="📥Download PDF",
                data=pdf_data,
                file_name='leave_balance_report.pdf',
                mime='application/pdf'
            )
    else:
        st.write("No leave balance data available.")



if selected_report == "Pending appointment letters":
    df_appointment_data = fetch_appointment_letters_data("Pending appointment letters",report_options, org_id)
    st.header("Pending Appointment Letters")
    if not df_appointment_data.empty:
        df_appointment_data['work_date_of_joining'] = df_appointment_data['work_date_of_joining'].apply(format_date)
        df_appointment_data = df_appointment_data.rename(columns={
            'full_name': 'Name',
            'work_departmentorg':'Hotel Name',
            'EmployeeCode': 'Emp Code',
            'work_department': 'Department',
            'work_designation': 'Designation',
            'work_date_of_joining': 'Date of Joining',
            'work_status': "Emp Status",
            'appointment_status': 'Status',
            
        })


        df_display = df_appointment_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        
        excel_data = convert_df_to_excel(df_appointment_data)
        pdf_data = create_pdf_report(df_appointment_data, "Pending appointment letters", selected_org)

      
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='appointment_letter_report.xlsx', 
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='appointment_letter_report.pdf', 
                               mime='application/pdf')
    else:
        st.write("No appointment data available.")


if selected_report == "Pending Confirmation Letters":
    df_confirmation_data = fetch_confirmation_letters_data("Pending Confirmation Letters",report_options, org_id,selected_department, selected_designation,)
    st.header("Pending Confirmation Letters")
    if not df_confirmation_data.empty:
        df_confirmation_data['work_date_of_joining'] = df_confirmation_data['work_date_of_joining'].apply(format_date)
        df_confirmation_data['Date of Confirmation'] = df_confirmation_data['Date of Confirmation'].apply(format_date)
        df_confirmation_data = df_confirmation_data.rename(columns={
            'full_name': 'Name',
            'EmployeeCode': 'Emp Code',
            'work_departmentorg':'Hotel Name',
            'work_department': 'Department',
            'work_designation': 'Designation',
            'work_date_of_joining': 'Date of Joining',
            'work_status': 'Status',
            'Date of Confirmation': 'Date of Confirmation',  
            'Remaining Days': 'Remaining Days',              
            'Confirmation Status': 'Confirmation Status'      
        })
        
        df_display = df_confirmation_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        
        excel_data = convert_df_to_excel(df_confirmation_data)
        pdf_data = create_pdf_report(df_confirmation_data, "Pending Confirmation Letters", selected_org)

        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='confirmation_letter_report.xlsx', 
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='confirmation_letter_report.pdf', 
                               mime='application/pdf')
    else:
        st.write("No confirmation data available.")



if selected_report == "Full and final pending with auditors report":
    
    df_full_and_final_data = fetch_full_and_final_data("Full and final pending with auditors report",report_options, org_id,selected_department, selected_designation, selected_year,  selected_months)

    if not df_full_and_final_data.empty:
        df_full_and_final_data['DOJ'] = df_full_and_final_data['DOJ'].apply(format_date)
        df_full_and_final_data['Date_Of_Leaving'] = df_full_and_final_data['Date_Of_Leaving'].apply(format_date)
        df_full_and_final_data = df_full_and_final_data.rename(columns={
            'Name': 'Name',
            'Emp_Code': 'Emp Code',
            'work_departmentorg':'Hotel Name',
            'Dept': 'Department',
            'Designation': 'Designation',
            'DOJ': 'Date of Joining',
            'Date_Of_Leaving': 'Date of Leaving',
            'Absconding': 'Absconding Status',
            'Notice_Days_Served': 'Notice Days Served',
            'AuditedBy': 'Audited By',
            'FinalStatus': 'Final Status',
        })

        st.header("Full and Final Pending with Auditors Report")
       
        df_full_and_final_data = df_full_and_final_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_full_and_final_data.reset_index(drop=True, inplace=True)
        df_full_and_final_data.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_full_and_final_data, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})

        
        excel_data = convert_df_to_excel(df_full_and_final_data)
        pdf_data = create_pdf_report(df_full_and_final_data, "Full and Final Pending with Auditors", selected_org)
    else:
        st.write("No Full and final pending with auditors report data available.")

elif selected_report == "Full and final pending with finance report":
    
    df_full_and_final_data = fetch_full_and_final_data("Full and final pending with finance report",report_options, org_id,selected_department, selected_designation, selected_year,  selected_months)

    if not df_full_and_final_data.empty:
        df_full_and_final_data['DOJ'] = df_full_and_final_data['DOJ'].apply(format_date)
        df_full_and_final_data['Date_Of_Leaving'] = df_full_and_final_data['Date_Of_Leaving'].apply(format_date)
        df_full_and_final_data = df_full_and_final_data.rename(columns={
            'Name': 'Name',
            'Emp_Code': 'Emp Code',
             'work_departmentorg':'Hotel Name',
            'Dept': 'Department',
            'Designation': 'Designation',
            'Date_Of_Leaving': 'Date of Leaving',
             'DOJ': 'Date of Joining',
            'Laid_Off': 'Laid Off Status',
            'Confirmed': 'Confirmation Status',
            'AuditedBy': 'Audited By',
            'PaymentStatus': 'Payment Status',
           
           
        })

        st.header("Full and Final Pending with Finance Report")

        df_full_and_final_data = df_full_and_final_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_full_and_final_data.reset_index(drop=True, inplace=True)
        df_full_and_final_data.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_full_and_final_data, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})

        excel_data = convert_df_to_excel(df_full_and_final_data)
        pdf_data = create_pdf_report(df_full_and_final_data, "Full and Final Pending with Finance", selected_org)
    else:
        st.write("No Full and final pending with finance report data available.")

elif selected_report == "Pending full and final report":
    
    df_full_and_final_data = fetch_full_and_final_data("Pending full and final report",report_options, org_id,selected_department, selected_designation, selected_year,  selected_months)

    if not df_full_and_final_data.empty:
        df_full_and_final_data['DOJ'] = df_full_and_final_data['DOJ'].apply(format_date)
        df_full_and_final_data['Date_Of_Leaving'] = df_full_and_final_data['Date_Of_Leaving'].apply(format_date)
        df_full_and_final_data = df_full_and_final_data.rename(columns={
            'Name': 'Name',
            'Emp_Code': 'Emp Code',
             'work_departmentorg':'Hotel Name',
            'Dept': 'Department',
            'Designation': 'Designation',
            'DOJ': 'Date of Joining',
            'Date_Of_Leaving': 'Date of Leaving',
            'Resignation': 'Resignation Status',
            'Current_Salary': 'Current Salary',
            'FinalStatus': 'Final Status',
            'PaymentStatus': 'Payment Status',
           
        })
        
        st.header("Pending Full and Final Report")
        
        df_full_and_final_data = df_full_and_final_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_full_and_final_data.reset_index(drop=True, inplace=True)
        df_full_and_final_data.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_full_and_final_data, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})

        
        excel_data = convert_df_to_excel(df_full_and_final_data)
        pdf_data = create_pdf_report(df_full_and_final_data, "Pending Full and Final", selected_org)
    else:
        st.write("No Pending full and final report data available.")

elif selected_report == "Full and final pending clearance report":
 
    df_full_and_final_data = fetch_full_and_final_data("Full and final pending clearance report",report_options, org_id,selected_department, selected_designation, selected_year,  selected_months)

    if not df_full_and_final_data.empty:
        df_full_and_final_data['DOJ'] = df_full_and_final_data['DOJ'].apply(format_date)
        df_full_and_final_data['Date_Of_Leaving'] = df_full_and_final_data['Date_Of_Leaving'].apply(format_date)
        df_full_and_final_data = df_full_and_final_data.rename(columns={
            'Name': 'Name',
            'Emp_Code': 'Emp Code',
             'work_departmentorg':'Hotel Name',
            'Dept': 'Department',
            'Designation': 'Designation',
            'DOJ': 'Date of Joining',
            'Date_Of_Leaving': 'Date of Leaving',
            'Terminated': 'Termination Status',
            'Confirmed': 'Confirmation Status',
            'PaymentStatus': 'Payment Status',
           
        })

        
        
        
        st.header("Full and Final Pending Clearance Report")
        df_full_and_final_data = df_full_and_final_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_full_and_final_data.reset_index(drop=True, inplace=True)
        df_full_and_final_data.index += 1
        
        # Display the DataFrame with a "View" column
        st.dataframe(df_full_and_final_data, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})

        
        excel_data = convert_df_to_excel(df_full_and_final_data)
        pdf_data = create_pdf_report(df_full_and_final_data, "Pending Clearance", selected_org)

    else:
        st.write("No Full and final pending clearance report data available.")



if selected_report == "Department wise manning report":
    
    df_manning_data = fetch_departmentmanning_names("Department wise manning report",report_options, org_id, selected_department, selected_designation)
  
    st.header("Department Wise Manning Report")
    if df_manning_data is not None and not df_manning_data.empty:
      
        df_manning_data = df_manning_data.rename(columns={
            'Dept': 'Department',
            'Designation': 'Designation',
            'employee_count': 'Employee Count',
             'work_departmentorg': 'Hotel Name',
        })

        
        
       
        df_manning_data.reset_index(drop=True, inplace=True)
        df_manning_data.index += 1
       
        st.dataframe(df_manning_data, width=1400)
       
        excel_data = convert_df_to_excel(df_manning_data)
        pdf_data = create_pdf_report(df_manning_data, "Department Wise Manning Report", selected_org)

        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='department_manning_report.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='department_manning_report.pdf',
                               mime='application/pdf')
    else:
        st.write("No Department Wise Manning Report available.")




if selected_report == "Attrition Report":
    attrition_data = fetch_budget_on_roll_data(
        "Attrition Report", report_options, org_id, selected_department, selected_designation
    )

    if attrition_data and isinstance(attrition_data, list) and len(attrition_data) > 0:
        # Convert data to a DataFrame
        try:
            df_Attrition_data = pd.DataFrame(attrition_data)
            df_Attrition_data = df_Attrition_data.fillna(0)
            df_Attrition_data = df_Attrition_data.rename(columns={
                'Dept': 'Department',
                'Designation': 'Designation',
                'employee_count': 'Employee Count',
                'JoinCount': 'Additions (Month)'
            })

            # Display header
            st.header("Attrition Report")

            # Reset and re-index
            df_Attrition_data.reset_index(drop=True, inplace=True)
            df_Attrition_data.index += 1

            # Display DataFrame
            st.dataframe(df_Attrition_data, width=1400)

            # Generate Excel and PDF
            excel_data = convert_df_to_excel(df_Attrition_data)
            pdf_data = create_pdf_report(df_Attrition_data, "Attrition Report", selected_org)

            # Add download buttons
            col1, col2 = st.sidebar.columns(2)
            with col1:
                st.download_button(
                    label="📥Download Excel", 
                    data=excel_data, 
                    file_name='department_Attrition_report.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            with col2:
                st.download_button(
                    label="📥Download PDF", 
                    data=pdf_data, 
                    file_name='department_Attrition_report.pdf',
                    mime='application/pdf'
                )
        except ValueError as e:
            st.write("Error processing data: ", str(e))
    else:
        # Display message when no data is available
        st.warning("Data not found for Attrition Report.")







# MASTER REPORT
from app.models import City_Location_Master  

import datetime
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from datetime import date, timedelta

# Assuming `EmployeeWorkDetails` model and other necessary setup are already in place
from dateutil.relativedelta import relativedelta

# def calculate_tenure_in_years(employee):
#     # Convert DateofJoining to datetime if it's a string and ensure proper format
#     if isinstance(employee.DateofJoining, str):
#         employee.DateofJoining = pd.to_datetime(employee.DateofJoining, errors='coerce')

#     # If DateofJoining is invalid (NaT), return None
#     if pd.isnull(employee.DateofJoining):
#         return None

#     # Add 6 months (approximately 180 days) to the DateofJoining to calculate the confirmation date
#     confirmation_date = employee.DateofJoining + relativedelta(months=6)  # Approximate 6 months
    
#     # Calculate tenure based on the confirmation date
#     today = date.today()
#     tenure_years = today.year - confirmation_date.year
#     tenure_months = today.month - confirmation_date.month
#     tenure_days = today.day - confirmation_date.day

#     if tenure_days < 0:
#         # Adjust by going back to the last day of the previous month
#         previous_month_last_day = (today.replace(day=1) - timedelta(days=1)).day
#         tenure_days += previous_month_last_day
#         tenure_months -= 1

#     if tenure_months < 0:
#         tenure_years -= 1
#         tenure_months += 12

#     # Return confirmation date and tenure in years
#     return confirmation_date, tenure_years
def calculate_tenure_in_years(employee):
    # Convert DateofJoining to datetime if it's a string and ensure proper format
    if isinstance(employee.DateofJoining, str):
        employee.DateofJoining = pd.to_datetime(employee.DateofJoining, errors='coerce')

    # If DateofJoining is invalid (NaT), return None
    if pd.isnull(employee.DateofJoining):
        return None

    # Calculate tenure in years
    today = date.today()
    tenure_years = today.year - employee.DateofJoining.year
    tenure_months = today.month - employee.DateofJoining.month
    tenure_days = today.day - employee.DateofJoining.day

    if tenure_days < 0:
        # Adjust by going back to the last day of the previous month
        previous_month_last_day = (today.replace(day=1) - timedelta(days=1)).day
        tenure_days += previous_month_last_day
        tenure_months -= 1

    if tenure_months < 0:
        tenure_years -= 1
        tenure_months += 12

    return tenure_years

def calculate_tenure_in_months(employee):
    # Convert DateofJoining to datetime if it's a string and ensure proper format
    if isinstance(employee.DateofJoining, str):
        employee.DateofJoining = pd.to_datetime(employee.DateofJoining, errors='coerce')

    # If DateofJoining is invalid (NaT), return None
    if pd.isnull(employee.DateofJoining):
        return None

    # Calculate tenure in years
    today = date.today()
    tenure_years = today.year - employee.DateofJoining.year
    tenure_months = today.month - employee.DateofJoining.month
    tenure_days = today.day - employee.DateofJoining.day

    if tenure_days < 0:
        # Adjust by going back to the last day of the previous month
        previous_month_last_day = (today.replace(day=1) - timedelta(days=1)).day
        tenure_days += previous_month_last_day
        tenure_months -= 1

    if tenure_months < 0:
        tenure_years -= 1
        tenure_months += 12

    return tenure_months

def calculate_tenure_str(employee):
    # Convert DateofJoining to datetime if it's a string
    if isinstance(employee.DateofJoining, str):
        employee.DateofJoining = pd.to_datetime(employee.DateofJoining, errors='coerce')

    # If invalid joining date
    if pd.isnull(employee.DateofJoining):
        return "0y 0m"

    today = date.today()
    tenure_years = today.year - employee.DateofJoining.year
    tenure_months = today.month - employee.DateofJoining.month
    tenure_days = today.day - employee.DateofJoining.day

    if tenure_days < 0:
        # Adjust for incomplete month
        previous_month_last_day = (today.replace(day=1) - timedelta(days=1)).day
        tenure_days += previous_month_last_day
        tenure_months -= 1

    if tenure_months < 0:
        tenure_years -= 1
        tenure_months += 12

    return f"{tenure_years}Y - {tenure_months}M"


from django.db.models import Case, When, Value, CharField, OuterRef, Subquery

from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models.functions import Coalesce
from HumanResources.models import EmployeeAddressInformationDetails,Salary_Detail_Master
from PADP.models import APADP
from ProbationConfirmation.models import Emp_Confirmation_Master
from LetteofPromotion.models import PromotionLetterEmployeeDetail

from LetterSalaryIncrement.models import LETTEROFSALARYINCREAMENTEmployeeDetail
from FullandFinalSettlement.models import Full_and_Final_Settltment
from Clearance_From.models import ClearenceEmp
from ExitInterview.models import Exitinterviewdata
from django.db.models.functions import ExtractYear
from django.db.models.functions import TruncDate

from django.db.models.expressions import RawSQL, Subquery, OuterRef
    

employees=[]
# print("fetch_masterreport_data of selected division is here::", selected_Division)
def fetch_masterreport_data(report_type, org_id, selected_Division, selected_department, selected_designation, selected_year, selected_months, selected_level, report_options):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Master Report":
        print("report type is here::", report_type)
        
        organization_name = get_organization_short_name(org_id)
        
        if org_id is None:
                     print("we are in If condition of", report_type)

                     employees = EmployeePersonalDetails.objects.annotate(
                        work_designation=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            
                        ).values('Designation')[:1]),
                      
                        work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                            OrganizationID=OuterRef('OrganizationID'),
                            IsDelete=False
                        ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                        work_departmentorg_id=Subquery(
                            OrganizationMaster.objects.filter(
                                OrganizationID=OuterRef('OrganizationID'),
                                IsDelete=False
                            ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                            ),  

                        work_department=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                        ).values('Department')[:1]),
                        
                        work_division=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                        ).values('Division')[:1]),

                        Level=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                        ).values('Level')[:1]),
                        
                        ReportingtoDepartment=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                        ).values('ReportingtoDepartment')[:1]),

                        ReportingtoDesignation=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                        ).values('ReportingtoDesignation')[:1]),

                        work_date_of_joining=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            
                        ).values('DateofJoining')[:1]),
                        work_status=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            
                        ).values('EmpStatus')[:1]),
                        full_name=Concat('FirstName', Value(' '), 'LastName'),
                        emergency_prefix=Subquery(EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('Prefix')[:1]),
                        emergency_contact_1=Subquery(EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('EmergencyContactNumber_1')[:1]),
                        emergency_contact_2=Subquery(EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('EmergencyContactNumber_2')[:1]),
                        blood_group=Subquery(EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('BloodGroup')[:1]),
                        Permanent_State=Subquery(EmployeeAddressInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('Permanent_State')[:1]),
                        Permanent_City=Subquery(EmployeeAddressInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('Permanent_City')[:1]),
                        ctc=Coalesce(
                            Subquery(
                                Salary_Detail_Master.objects.filter(
                                    EmpID=OuterRef('EmpID'),
                                    Salary_title__Title__icontains="ctc",  
                                    IsDelete=False
                                ).values('Permonth')[:1]
                            ),
                            0,  
                            output_field=DecimalField() 
                        ),
                        
                        
                        emp_code_match=Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                               IsDelete=False
                            ).values('emp_code')[:1]
                        ),
                        empappoinment_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False,
                            )
                            .annotate(
                                date_only=RawSQL("try_cast(date_of_appointment AS DATE)", [])
                            )
                            .values('date_only')[:1]
                        ),
                        Issuing_manager_name_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('Issuing_manager_name')[:1]  
                        ),
                        BasicSalary_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('basic_salary')[:1]  
                        ),
                        HRName_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('Hr_Name')[:1]  
                        ),
                        HRDesignation_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('Hr_Designation')[:1]  
                        ),
                        IssuingDesignation_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('Issuing_designation')[:1]  
                        ),
                       
                        status=Case(
                            When(emp_code_match__isnull=False, then=Value('Signed Document Uploaded')),
                            default=Value('Pending'),
                            output_field=CharField()
                        ),
                        # probation_confirmation
                        probation_match=Subquery(
                            Emp_Confirmation_Master.objects.filter(
                                EmpCode=OuterRef('EmployeeCode'),IsDelete=False, 
                               
                            ).values('EmpConfirm')[:1]
                        ),
                        probationstatus = Case(
                            When(probation_match=0, then=Value('Pending')), 
                            When(probation_match=1, then=Value('Confirmed')),  
                            default=Value('Pending'),  # Default value if no match is found
                            output_field=CharField()
                        ),
                        Extended_match = Coalesce(
                            Subquery(
                                Emp_Confirmation_Master.objects.filter(
                                    EmpCode=OuterRef('EmployeeCode'),
                                    IsDelete=False,
                                    
                                ).values('Extended')[:1]
                            ),
                            Value('None')  # Default value when no match is found
                        ),
                        ConfDate_match=Subquery(
                            Emp_Confirmation_Master.objects.filter(
                                EmpCode=OuterRef('EmployeeCode'),IsDelete=False, 
                                
                            ).values('ConfDate')[:1]
                        ),
                        
                        promotion_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False, 
                                
                            ).values('emp_code')[:1]
                        ),
                        promotionstatus=Case(
                            When(promotion_match__isnull=False, then=Value('Issued')),  # If 
                            default=Value('Pending'),
                            
                            output_field=CharField() 
                        ),
                        dateofpromotion_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False,
                               
                            ).values('date_of_promtion')[:1]
                        ),
                         Promotiondesignation_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False,
                                
                            ).values('Promotiondesignation')[:1]
                        ),
                         Issuing_managerPromotion_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False,
                                
                            ).values('Issuing_manager_name')[:1]
                        ),
                         Issuing_designationPromotion_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False,
                                
                            ).values('Issuing_designation')[:1]
                        ),
                    #    resignation module 
                        empresigantions = Subquery(
                                EmpResigantionModel.objects.filter(
                                    Emp_Code=OuterRef('EmployeeCode'),  
                                                  
                                    
                                    IsDelete=False              
                                ).values('Emp_Code')[:1]      
                            ),

                            
                        resignationstatus = Case(
                                When(empresigantions__isnull=False, then=Value('Approved')), 
                                default=Value('Pending for Approval'),  
                                output_field=CharField()  
                            ),
                        resigntionsdate = Subquery(
                                EmpResigantionModel.objects.filter(
                                    Emp_Code=OuterRef('EmployeeCode'),
                                    IsDelete=False,
                                )
                                .annotate(
                                    date_only=RawSQL("try_cast(Date_Of_res AS DATE)", [])
                                )
                                .values('date_only')[:1]
                            ),
                        typeofresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('TypeofRes')[:1]  
                        ),
                        NoticePeriodresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('NoticePeriod')[:1]  
                        ),
                        Reasonresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('Res_Reason')[:1]  
                        ),
                        Ressubmittedtoresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('Ressubmittedto')[:1]  
                        ),
                        Res_acceptance_Dateresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('Res_acceptance_Date')[:1]  
                        ),
                        Res_acceptance_Byresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            )
                            .values('Res_acceptance_By')[:1]  
                        ),           
                        salaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('emp_code')[:1]
                        ),
                        salaryincrementstatus=Case(
                            When(salaryincrement_match__isnull=False, then=Value('Issued')),  # If 
                            default=Value('Pending'),  
                            output_field=CharField() 
                        ),
                        date_of_salarysalaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                               IsDelete=False
                            ).values('date_of_salary_increament')[:1]
                        ),
                        CTCsalaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('CTC')[:1]
                        ),
                        Issuing_manager_namesalaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('Issuing_manager_name')[:1]
                        ),
                        Issuing_designationsalaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('Issuing_designation')[:1]
                        ),
                        fnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('Emp_Code')[:1]
                        ),
                        fnfstatus=Case(
                            When(fnf_match__isnull=False, then=Value('Issued')),  # If 
                            default=Value('Pending'),  
                            output_field=CharField() 
                        ),
                        AuditedByfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('AuditedBy')[:1]
                        ),
                        PaymentStatusfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('PaymentStatus')[:1]
                        ),
                        FinalStatusfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                               IsDelete=False
                            ).values('FinalStatus')[:1]
                        ),
                        Date_Of_Leavingfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('Date_Of_Leaving')[:1]
                        ),
                         Abscondingfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('Absconding')[:1]
                        ),
                         Resignationfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('Resignation')[:1]
                        ),
                         Terminatedfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('Terminated')[:1]
                        ),
                         PaymentPaidAmountfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('PaymentPaidAmount')[:1]
                        ),
                        Clearence_match=Subquery(
                            ClearenceEmp.objects.filter(
                                EmpCode=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('EmpCode')[:1]
                        ),
                        Clearencestatus=Case(
                            When(Clearence_match__isnull=False, then=Value('Issued')),  # If 
                            default=Value('Pending'),  
                            output_field=CharField() 
                        ),
                        SeparationDateClearence_match=Subquery(
                            ClearenceEmp.objects.filter(
                                EmpCode=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('SeparationDate')[:1]
                        ),
                        Exitinterview_match=Subquery(
                            Exitinterviewdata.objects.filter(
                                Employee_Code=OuterRef('EmployeeCode'),
                               IsDelete=False
                            ).values('Employee_Code')[:1]
                        ),
                        Exitinterviewstatus=Case(
                            When(Exitinterview_match__isnull=False, then=Value('Complete')), 
                            default=Value('Pending'),  
                            output_field=CharField() 
                        ),
                        DateofLeavingExitinterview_match=Subquery(
                            Exitinterviewdata.objects.filter(
                                Employee_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('DateofLeaving')[:1]
                        ),
                         ReasonForLeavingExitinterview_match=Subquery(
                            Exitinterviewdata.objects.filter(
                                Employee_Code=OuterRef('EmployeeCode'),
                               IsDelete=False
                            ).values('ReasonForLeaving')[:1]
                        ),
                        NoticePeriodExitinterview_match=Subquery(
                            Exitinterviewdata.objects.filter(
                                Employee_Code=OuterRef('EmployeeCode'),
                                IsDelete=False
                            ).values('NoticePeriod')[:1]
                        ),
                    
                    ).filter(IsDelete=False,)
        else:
                print(f"we are in else condition of hello {report_type}")
                employees = EmployeePersonalDetails.objects.annotate(
                        work_designation=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            OrganizationID=org_id
                        ).values('Designation')[:1]),
                         work_departmentorg=Subquery(OrganizationMaster.objects.filter(
                            OrganizationID=OuterRef('OrganizationID'),
                            IsDelete=False
                        ).order_by('ShortDisplayLabel').values('ShortDisplayLabel')[:1]),
                        work_departmentorg_id=Subquery(
                        OrganizationMaster.objects.filter(
                            OrganizationID=OuterRef('OrganizationID'),
                            IsDelete=False
                        ).order_by('ShortDisplayLabel').values('OrganizationID')[:1]
                        ),  
                        work_department=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            OrganizationID=org_id
                        ).values('Department')[:1]),
                        work_division=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            OrganizationID=org_id
                        ).values('Division')[:1]),
                        Level=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            OrganizationID=org_id
                        ).values('Level')[:1]),

                        ReportingtoDepartment=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            OrganizationID=org_id
                        ).values('ReportingtoDepartment')[:1]),

                        ReportingtoDesignation=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            OrganizationID=org_id
                        ).values('ReportingtoDesignation')[:1]),
                        
                        work_date_of_joining=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            OrganizationID=org_id
                        ).values('DateofJoining')[:1]),
                        work_status=Subquery(EmployeeWorkDetails.objects.filter(
                            EmpID=OuterRef('EmpID'),
                            IsDelete=False,
                            OrganizationID=org_id
                        ).values('EmpStatus')[:1]),
                        full_name=Concat('FirstName', Value(' '), 'LastName'),
                        emergency_prefix=Subquery(EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('Prefix')[:1]),
                        emergency_contact_1=Subquery(EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('EmergencyContactNumber_1')[:1]),
                        emergency_contact_2=Subquery(EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('EmergencyContactNumber_2')[:1]),
                        blood_group=Subquery(EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('BloodGroup')[:1]),
                        Permanent_State=Subquery(EmployeeAddressInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('Permanent_State')[:1]),
                        Permanent_City=Subquery(EmployeeAddressInformationDetails.objects.filter(EmpID=OuterRef('EmpID')).values('Permanent_City')[:1]),
                        ctc=Coalesce(
                            Subquery(
                                Salary_Detail_Master.objects.filter(
                                    EmpID=OuterRef('EmpID'),
                                    Salary_title__Title__icontains="ctc",  
                                    IsDelete=False
                                ).values('Permonth')[:1]
                            ),
                            0,  
                            output_field=DecimalField() 
                        ),
                        
                        
                        emp_code_match=Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('emp_code')[:1]
                        ),
                        empappoinment_match = Subquery(
                                LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                    emp_code=OuterRef('EmployeeCode'),
                                    IsDelete=False,
                                    OrganizationID=org_id,
                                )
                                .annotate(
                                    date_only=RawSQL("try_cast(date_of_appointment AS DATE)", [])
                                )
                                .values('date_only')[:1]
                            ),
                        Issuing_manager_name_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('Issuing_manager_name')[:1]  
                        ),
                        BasicSalary_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('basic_salary')[:1]  
                        ),
                        HRName_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('Hr_Name')[:1]  
                        ),
                        HRDesignation_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('Hr_Designation')[:1]  
                        ),
                        IssuingDesignation_match = Subquery(
                            LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('Issuing_designation')[:1]  
                        ),
                       
                        status=Case(
                            When(emp_code_match__isnull=False, then=Value('Signed Document Uploaded')),
                            default=Value('Pending'),
                            output_field=CharField()
                        ),
                        # probation_confirmation
                        probation_match=Subquery(
                            Emp_Confirmation_Master.objects.filter(
                                EmpCode=OuterRef('EmployeeCode'),IsDelete=False, 
                                OrganizationID=org_id
                            ).values('EmpConfirm')[:1]
                        ),
                        probationstatus = Case(
                            When(probation_match=0, then=Value('Pending')), 
                            When(probation_match=1, then=Value('Confirmed')),  
                            default=Value('Pending'),  
                            output_field=CharField()
                        ),
                        Extended_match = Coalesce(
                            Subquery(
                                Emp_Confirmation_Master.objects.filter(
                                    EmpCode=OuterRef('EmployeeCode'),
                                    IsDelete=False,
                                    OrganizationID=org_id
                                ).values('Extended')[:1]
                            ),
                            Value('None')  
                        ),
                        ConfDate_match=Subquery(
                            Emp_Confirmation_Master.objects.filter(
                                EmpCode=OuterRef('EmployeeCode'),IsDelete=False, 
                                OrganizationID=org_id
                            ).values('ConfDate')[:1]
                        ),
                        
                        promotion_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False, 
                                OrganizationID=org_id
                            ).values('emp_code')[:1]
                        ),
                        promotionstatus=Case(
                            When(promotion_match__isnull=False, then=Value('Issued')),  # If 
                            default=Value('Pending'),
                            
                            output_field=CharField() 
                        ),
                        dateofpromotion_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False,
                                OrganizationID=org_id
                            ).values('date_of_promtion')[:1]
                        ),
                         Promotiondesignation_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False,
                                OrganizationID=org_id
                            ).values('Promotiondesignation')[:1]
                        ),
                         Issuing_managerPromotion_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False,
                                OrganizationID=org_id
                            ).values('Issuing_manager_name')[:1]
                        ),
                         Issuing_designationPromotion_match=Subquery(
                            PromotionLetterEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),IsDelete=False,
                                OrganizationID=org_id
                            ).values('Issuing_designation')[:1]
                        ),
                    #    resignation module 
                        empresigantions = Subquery(
                                EmpResigantionModel.objects.filter(
                                    Emp_Code=OuterRef('EmployeeCode'),  
                                                  
                                    OrganizationID=org_id,
                                    IsDelete=False              
                                ).values('Emp_Code')[:1]      
                            ),

                            
                        resignationstatus = Case(
                                When(empresigantions__isnull=False, then=Value('Approved')), 
                                default=Value('Pending for Approval'),  
                                output_field=CharField()  
                            ),
                        resigntionsdate = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                IsDelete=False,
                                OrganizationID=org_id,
                            )
                            .annotate(
                                date_only=RawSQL("try_cast(Date_Of_res AS DATE)", [])
                            )
                            .values('date_only')[:1]
                        ),
                        typeofresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('TypeofRes')[:1]  
                        ),
                        NoticePeriodresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('NoticePeriod')[:1]  
                        ),
                        Reasonresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('Res_Reason')[:1]  
                        ),
                        Ressubmittedtoresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('Ressubmittedto')[:1]  
                        ),
                        Res_acceptance_Dateresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('Res_acceptance_Date')[:1]  
                        ),
                        Res_acceptance_Byresigntions_match = Subquery(
                            EmpResigantionModel.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            )
                            .values('Res_acceptance_By')[:1]  
                        ),           
                        salaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('emp_code')[:1]
                        ),
                        salaryincrementstatus=Case(
                            When(salaryincrement_match__isnull=False, then=Value('Issued')),  # If 
                            default=Value('Pending'),  
                            output_field=CharField() 
                        ),
                        date_of_salarysalaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('date_of_salary_increament')[:1]
                        ),
                        CTCsalaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('CTC')[:1]
                        ),
                        Issuing_manager_namesalaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('Issuing_manager_name')[:1]
                        ),
                        Issuing_designationsalaryincrement_match=Subquery(
                            LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
                                emp_code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('Issuing_designation')[:1]
                        ),
                        fnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('Emp_Code')[:1]
                        ),
                        fnfstatus=Case(
                            When(fnf_match__isnull=False, then=Value('Issued')),  # If 
                            default=Value('Pending'),  
                            output_field=CharField() 
                        ),
                        AuditedByfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('AuditedBy')[:1]
                        ),
                        PaymentStatusfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('PaymentStatus')[:1]
                        ),
                        FinalStatusfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('FinalStatus')[:1]
                        ),
                        Date_Of_Leavingfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('Date_Of_Leaving')[:1]
                        ),
                         Abscondingfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('Absconding')[:1]
                        ),
                         Resignationfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('Resignation')[:1]
                        ),
                         Terminatedfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('Terminated')[:1]
                        ),
                         PaymentPaidAmountfnf_match=Subquery(
                            Full_and_Final_Settltment.objects.filter(
                                Emp_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('PaymentPaidAmount')[:1]
                        ),
                        Clearence_match=Subquery(
                            ClearenceEmp.objects.filter(
                                EmpCode=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('EmpCode')[:1]
                        ),
                        Clearencestatus=Case(
                            When(Clearence_match__isnull=False, then=Value('Issued')),  # If 
                            default=Value('Pending'),  
                            output_field=CharField() 
                        ),
                        SeparationDateClearence_match=Subquery(
                            ClearenceEmp.objects.filter(
                                EmpCode=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('SeparationDate')[:1]
                        ),
                        Exitinterview_match=Subquery(
                            Exitinterviewdata.objects.filter(
                                Employee_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('Employee_Code')[:1]
                        ),
                        Exitinterviewstatus=Case(
                            When(Exitinterview_match__isnull=False, then=Value('Complete')), 
                            default=Value('Pending'),  
                            output_field=CharField() 
                        ),
                        DateofLeavingExitinterview_match=Subquery(
                            Exitinterviewdata.objects.filter(
                                Employee_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('DateofLeaving')[:1]
                        ),
                         ReasonForLeavingExitinterview_match=Subquery(
                            Exitinterviewdata.objects.filter(
                                Employee_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('ReasonForLeaving')[:1]
                        ),
                        NoticePeriodExitinterview_match=Subquery(
                            Exitinterviewdata.objects.filter(
                                Employee_Code=OuterRef('EmployeeCode'),
                                OrganizationID=org_id,IsDelete=False
                            ).values('NoticePeriod')[:1]
                        ),
                    
                    ).filter(IsDelete=False, OrganizationID=org_id)
                
 
        if selected_Division != 'All':#vasudev
            employees = employees.filter(work_division=selected_Division)
            # data = data.filter(Division=selected_Division)

        if selected_department != 'All':
            employees = employees.filter(work_department=selected_department)
        

        if selected_designation != 'All':
            employees = employees.filter(work_designation=selected_designation)

        if selected_level != 'All':  
            employees = employees.filter(Level=selected_level)
        
        employees = employees.filter(
            work_date_of_joining__year__in=selected_year,
            work_date_of_joining__month__in=[months.index(month) + 1 for month in selected_months],
           
        )

        employees = employees.exclude(EmployeeCode__isnull=True).exclude(EmployeeCode__exact='')

        
        df = pd.DataFrame(list(employees.values(
            'work_departmentorg','EmployeeCode','full_name', 'work_division',
            'work_department', 'work_designation', 'ReportingtoDesignation',
            'work_date_of_joining', 'work_status', "Gender", "Level", "age", "blood_group", "emergency_contact_1",
            "Permanent_State", "Permanent_City", 'ctc','status','probationstatus','promotionstatus','resignationstatus','salaryincrementstatus','fnfstatus','Clearencestatus','Exitinterviewstatus','emp_code_match','empappoinment_match','Issuing_manager_name_match','IssuingDesignation_match',
             'HRName_match','HRDesignation_match','BasicSalary_match','resigntionsdate','typeofresigntions_match',
            'NoticePeriodresigntions_match','work_departmentorg_id','EmpID',
            'Reasonresigntions_match',
            'Ressubmittedtoresigntions_match',
            'Res_acceptance_Dateresigntions_match',
            'Res_acceptance_Byresigntions_match',
            'Extended_match','ConfDate_match','dateofpromotion_match','Promotiondesignation_match',
            'Issuing_managerPromotion_match','Issuing_designationPromotion_match','date_of_salarysalaryincrement_match','CTCsalaryincrement_match','Issuing_manager_namesalaryincrement_match','Issuing_designationsalaryincrement_match','AuditedByfnf_match','FinalStatusfnf_match','PaymentStatusfnf_match','Date_Of_Leavingfnf_match','Abscondingfnf_match','Resignationfnf_match','Terminatedfnf_match','PaymentPaidAmountfnf_match',
            'SeparationDateClearence_match','DateofLeavingExitinterview_match','ReasonForLeavingExitinterview_match','NoticePeriodExitinterview_match'
        )))
       
        if 'work_departmentorg' not in df.columns:
            print("Data not found for 'work_departmentorg'")
        else:
            # Sort the DataFrame by 'work_departmentorg' if the column exists
            df = df.sort_values(by='work_departmentorg', ascending=True) 
        if org_id ==  None:
           
            desired_order = [
                
                'work_departmentorg','EmployeeCode', 'full_name', 'work_division', 'work_department', 'work_designation', 'Level','ReportingtoDesignation', 
                'work_date_of_joining', 'work_status', 'Gender', 'age', 'blood_group', "emergency_contact_1", "Permanent_State", "Permanent_City", 'ctc','status','probationstatus','promotionstatus','resignationstatus','salaryincrementstatus','fnfstatus','Clearencestatus','Exitinterviewstatus','empappoinment_match','Issuing_manager_name_match','IssuingDesignation_match','HRName_match','HRDesignation_match','BasicSalary_match','resigntionsdate',

                'typeofresigntions_match',
                'NoticePeriodresigntions_match',
                'Reasonresigntions_match','work_departmentorg_id','EmpID',
                'Ressubmittedtoresigntions_match',
                'Res_acceptance_Dateresigntions_match',
                'Res_acceptance_Byresigntions_match',
                 'Extended_match','ConfDate_match','dateofpromotion_match','Promotiondesignation_match','Issuing_managerPromotion_match','Issuing_designationPromotion_match','date_of_salarysalaryincrement_match','CTCsalaryincrement_match',
                 'Issuing_manager_namesalaryincrement_match','Issuing_designationsalaryincrement_match','AuditedByfnf_match','FinalStatusfnf_match','PaymentStatusfnf_match','Date_Of_Leavingfnf_match','Abscondingfnf_match','Resignationfnf_match','Terminatedfnf_match','PaymentPaidAmountfnf_match',
                  'SeparationDateClearence_match','DateofLeavingExitinterview_match','ReasonForLeavingExitinterview_match','NoticePeriodExitinterview_match'
          
            ]
        else:
            # df.insert(0, 'Hotel Name', organization_name)
            
            desired_order = [
                
                'work_departmentorg','EmployeeCode', 'full_name', 'work_division', 'work_department', 'work_designation', 'Level', 'ReportingtoDesignation', 
                'work_date_of_joining', 'work_status', 'Gender', 'age', 'blood_group', "emergency_contact_1", "Permanent_State", "Permanent_City", 'ctc','status','probationstatus','promotionstatus','resignationstatus','salaryincrementstatus','fnfstatus','Clearencestatus','Exitinterviewstatus','empappoinment_match','Issuing_manager_name_match','IssuingDesignation_match','HRName_match','HRDesignation_match','BasicSalary_match','resigntionsdate',

                'typeofresigntions_match',
                'NoticePeriodresigntions_match',
                'Reasonresigntions_match',
                'Ressubmittedtoresigntions_match','work_departmentorg_id','EmpID',
                'Res_acceptance_Dateresigntions_match',
                'Res_acceptance_Byresigntions_match',
                 'Extended_match','ConfDate_match','dateofpromotion_match','Promotiondesignation_match','Issuing_managerPromotion_match','Issuing_designationPromotion_match','date_of_salarysalaryincrement_match','CTCsalaryincrement_match',
                 'Issuing_manager_namesalaryincrement_match','Issuing_designationsalaryincrement_match','AuditedByfnf_match','FinalStatusfnf_match','PaymentStatusfnf_match','Date_Of_Leavingfnf_match','Abscondingfnf_match','Resignationfnf_match','Terminatedfnf_match','PaymentPaidAmountfnf_match',
                  'SeparationDateClearence_match','DateofLeavingExitinterview_match','ReasonForLeavingExitinterview_match','NoticePeriodExitinterview_match'
            ]
        
       
        for col in desired_order:
            if col not in df.columns:
                df[col] = None
        
        df = df[desired_order]
       
        PyHost = MasterAttribute.PyHost
        df['View'] = df.apply(
            lambda row: f"{PyHost}HumanResources/EditEmployee/?EmpID={encrypt_id(row['EmpID'])}&OID={row['work_departmentorg_id']}", axis=1
        )
        return df

    else:
        return None

from datetime import datetime

# Function to format dates
# import pandas as pd
# from datetime import datetime

# # Function to fetch data (assuming fetch_masterreport_data is defined elsewhere)
# def fetch_masterreport_data(report_type, org_id, department, designation, year, months, level, options):
#     # Replace with actual logic to fetch data
#     return pd.DataFrame()  # Example placeholder

# # Main logic for "Master Report"
# if selected_report == "Master Report":
#     st.sidebar.title("Filters for Master Report")
    
#     # Fetch the data
#     master_data = fetch_masterreport_data(
#         "Master Report",
#         org_id,
#         selected_department,
#         selected_designation,
#         selected_year,
#         selected_months,
#         selected_level,
#         report_options  
#     )

#     # Define columns to format
#     columns_to_format = [
#         'work_date_of_joining', 'empappoinment_match', 'resigntionsdate',
#         'Res_acceptance_Dateresigntions_match', 'ConfDate_match', 
#         'dateofpromotion_match', 'date_of_salarysalaryincrement_match',
#         'Date_Of_Leavingfnf_match', 'SeparationDateClearence_match', 'empappoinment_date_year'
#     ]

#     # Function to format date columns
#     def format_date_column(df, columns):
#         for column in columns:
#             if column in df.columns:
#                 # Convert to datetime and format
#                 df[column] = pd.to_datetime(df[column], errors='coerce').dt.strftime('%d %b %Y')
#         return df

#     # Apply the formatting function
#     master_data = format_date_column(master_data, columns_to_format)

#     # Log any missing columns for debugging
#     missing_columns = [col for col in columns_to_format if col not in master_data.columns]
#     if missing_columns:
#         print(f"Skipped formatting for missing columns: {missing_columns}")

#     # Display or process the formatted DataFrame
#     st.write("Formatted Master Report Data", master_data)


if selected_report == "Master Report":
    st.sidebar.title("Filters for Master Report")
    
    
    master_data = fetch_masterreport_data(
        "Master Report",
        org_id,
        selected_Division,
        selected_department,
        selected_designation,
        selected_year,
        selected_months,
        selected_level,
        report_options  
    )
    def format_date(date_value):
        try:
            
            return datetime.strptime(str(date_value), "%Y-%m-%d").strftime("%d %b %Y")
        except (ValueError, TypeError):
           
            return date_value

   
    columns_to_format = [
        'work_date_of_joining', 'empappoinment_match', 'resigntionsdate',
        'Res_acceptance_Dateresigntions_match', 'ConfDate_match', 
        'dateofpromotion_match', 'date_of_salarysalaryincrement_match',
        'Date_Of_Leavingfnf_match', 'SeparationDateClearence_match','empappoinment_date_year'
    ]

    for column in columns_to_format:
        if column in master_data.columns:
            master_data[column] = master_data[column].apply(format_date)
            
    master_data = master_data.rename(columns={
        'EmployeeCode': 'Emp Code',
        'full_name': 'Name',
        'work_department': 'Department',
        'work_division': 'Division',
        'work_departmentorg':'Hotel Name',
        'work_designation': 'Designation',
        'work_date_of_joining': 'DateofJoining',
        'work_status': 'Status',
        # 'ReportingtoDepartment': 'Reporting To',
        # 'ReportingtoDepartment': 'Reporting To',
        'ReportingtoDesignation': 'Reporting To Designation',
        'Hotel Name': 'Hotel Name',
        'Gender': 'Gender',
        'age': 'Age',
        'blood_group':'Blood Group',
        'emergency_contact_1':'Emergency Contact',
        'Permanent_State':'State',
        "Permanent_City":'City',
        "ctc":'CTC',
        'status':'Appointment Letter',
        'probationstatus':'Probation Confirmation',
        'promotionstatus':'Letter of Promotion',
        'resignationstatus': 'Resignation',
        'salaryincrementstatus':'Letter of Salary Increment',
        'fnfstatus':'FNF',
        'Clearencestatus':'Clearence Status',
        'Exitinterviewstatus':'Exit Interview Status',
        'empappoinment_match':'Appointment Date',
        'empappoinment_date_year':'empappoinment_date_year',
        'Issuing_manager_name_match':'Issuing Manager name',
        'BasicSalary_match':'Basic Salary','HRName_match':'HR Name','HRDesignation_match':'HR Designation','IssuingDesignation_match':'Issuing Designation',
         'resigntionsdate':'Resignation Date',
         'typeofresigntions_match':'Type of Resignation',
        'NoticePeriodresigntions_match':'Notice Period ',
        'Reasonresigntions_match':'Reason of Resignation',
        'Ressubmittedtoresigntions_match':'Resignation Submitted',
        'Res_acceptance_Dateresigntions_match':'Resignation Acceptance Date',
        'Res_acceptance_Byresigntions_match':'Resignation Acceptance',
        'Extended_match': 'Extended Confirmations',
        'ConfDate_match': 'Confirmations Date','dateofpromotion_match':'Date of Promotion','Promotiondesignation_match':'Promotion Designation',
         'Issuing_managerPromotion_match':'Issuing Manager Promotion','Issuing_designationPromotion_match':'Issuing Designation Promotion',
         'date_of_salarysalaryincrement_match':'Salary Increment Date','CTCsalaryincrement_match':'Salary Increment CTC','Issuing_manager_namesalaryincrement_match':'Issuing Manager Name','Issuing_designationsalaryincrement_match':'Issuing Designations',
         'AuditedByfnf_match':'Audited By','FinalStatusfnf_match':'Final Status','PaymentStatusfnf_match':'Payment Status','Date_Of_Leavingfnf_match':'Date of Leaving',
         'Abscondingfnf_match':'Absconding','Resignationfnf_match':'Resignations','Terminatedfnf_match':'Terminated','PaymentPaidAmountfnf_match':'Payment paid Amount', 'SeparationDateClearence_match':'Separation Date',
         'DateofLeavingExitinterview_match': 'Leaving Date','ReasonForLeavingExitinterview_match':'Reason Leaving','NoticePeriodExitinterview_match':'Notice period'
    })
    
    
       
    EmpCode = st.sidebar.text_input("Employee Code", "")
    first_name = st.sidebar.text_input("Employee Name", "")

    
    if EmpCode:
        master_data = master_data[master_data['Emp Code'].str.contains(EmpCode, case=False, na=False)]

    if first_name:
        master_data = master_data[master_data['Name'].str.contains(first_name, case=False, na=False)]
    
    emp_status = st.sidebar.selectbox(
        "Emp Status", 
        ["All", "Not Confirmed", "Confirmed", "On Probation", "Resigned", "Terminate", "F&F In process", "Absconding", "Archive", "Left", "F&F Completed"]
    )

    
    if emp_status == "All":
       
        master_data = master_data[master_data['Status'].isin(["Confirmed", "On Probation", "Not Confirmed"])]
    else:
        
        master_data = master_data[master_data['Status'] == emp_status]
  


    blood_group = st.sidebar.selectbox("Blood Group", ["All", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    if blood_group != "All":
        master_data = master_data[master_data['Blood Group'] == blood_group]
    else:
        master_data = master_data.drop(columns=['Blood Group'], errors='ignore')

    gender = st.sidebar.radio("Gender", ["All", "Male", "Female", "Other"])
    if gender != "All":
        master_data = master_data[master_data['Gender'] == gender]
    else:
        master_data = master_data.drop(columns=['Gender'], errors='ignore')
    
    show_emergency_contact = st.sidebar.checkbox("Emergency Contact")
    if show_emergency_contact:
        if 'Emergency Contact' not in master_data.columns:
            st.sidebar.warning("Emergency Contact column is missing in the data.")
    else:
        master_data = master_data.drop(columns=['Emergency Contact'], errors='ignore')
    
    min_age = 0
    max_age = 100
    
    if 'Age' in master_data.columns:
        
        master_data['Age'] = pd.to_numeric(master_data['Age'], errors='coerce')
        
       
        master_data = master_data.dropna(subset=['Age'])

        
        if not master_data['Age'].empty:
            
            min_age = master_data['Age'].min()
            max_age = master_data['Age'].max()

            
            if pd.notna(min_age) and pd.notna(max_age):
                max_age = int(max_age) + 1  
                min_age = int(min_age)  

                
                age_range = st.sidebar.slider("Age Range (Years)", min_value=min_age, max_value=max_age, value=(min_age, max_age), step=1)

                
                if age_range != (min_age, max_age):
                    master_data = master_data[(master_data['Age'] >= age_range[0]) & (master_data['Age'] <= age_range[1])]
            else:
                st.sidebar.warning("Invalid data for Age. Please check the data for inconsistencies.")
                
                age_range = (0, 0)
        else:
            st.sidebar.warning("No valid age data available after filtering out NaN values.")
            
            age_range = (0, 0)
    else:
        st.sidebar.warning("Age column is missing in the data.")
       
        age_range = (0, 0)

        
   
    if 'Age' in master_data.columns and age_range == (min_age, max_age):
        master_data = master_data.drop(columns=['Age'])


    master_data['Work Duration'] = master_data.apply(calculate_tenure_str, axis=1)

    # Remove the old numeric columns
    master_data = master_data.drop(columns=['Work Duration (Years)', 'Work Duration (Months)'], errors='ignore')

    
    # if 'Work Duration (Years)' not in master_data.columns:
    #     master_data['Work Duration (Years)'] = master_data.apply(calculate_tenure_in_years, axis=1)

   
    # work_duration = st.sidebar.slider("Work Duration (Years)", min_value=0, max_value=50, value=(0, 10), step=1)


    # if 'Work Duration (Months)' not in master_data.columns:
    #     master_data['Work Duration (Months)'] = master_data.apply(calculate_tenure_in_months, axis=1)

   
    # work_duration = st.sidebar.slider("Work Duration (Months)", min_value=0, max_value=50, value=(0, 10), step=1)

   
    # if work_duration != (0, 10):  
    #     min_duration, max_duration = work_duration  # Ensure work_duration is a tuple here
    #     master_data = master_data[
    #         (master_data['Work Duration (Years)'] >= min_duration) & 
    #         (master_data['Work Duration (Years)'] <= max_duration)
    #     ]
    # else:  
    #     # master_data = master_data.drop(columns=['Work Duration (Years)'], errors='ignore')
    #     pass

    

    if 'CTC' in master_data.columns:
        master_data['CTC'] = pd.to_numeric(master_data['CTC'], errors='coerce')
        master_data = master_data.dropna(subset=['CTC'])

        if not master_data['CTC'].empty:
            min_ctc, max_ctc = int(master_data['CTC'].min()), int(master_data['CTC'].max()) + 1000
            ctc_range = st.sidebar.slider("CTC Range", min_value=min_ctc, max_value=max_ctc, value=(min_ctc, max_ctc), step=1000)
            
            master_data = master_data[(master_data['CTC'] >= ctc_range[0]) & (master_data['CTC'] <= ctc_range[1])]
        else:
            st.sidebar.warning("No valid CTC data available after filtering out NaN values.")
    else:
        st.sidebar.warning("CTC column is missing in the data.")
       
    states = City_Location_Master.objects.values_list('StateName', flat=True).distinct().order_by('StateName')
    states = list(states)
    
    states = [state.title() for state in states]

    selected_state = st.sidebar.selectbox("Select State", ["Select a State"] + states)

    
    cities_selected = []
    if selected_state != "Select a State":
        cities_selected = City_Location_Master.objects.filter(StateName=selected_state).values_list('DistrictName', flat=True).distinct()
        cities_selected = list(cities_selected)
        
        
        cities_selected = [city.title() for city in cities_selected]

    selected_city = st.sidebar.selectbox("Select City", ["Select a City"] + cities_selected)
  
    
   
    if selected_state != "Select a State":
        if 'State' in master_data.columns:
            master_data = master_data[master_data['State'] == selected_state]
        else:
            st.sidebar.warning("State column is missing in the data.")
    else:
        master_data = master_data.drop(columns=['State'], errors='ignore')  

   
    if selected_city != "Select a City":
        if 'City' in master_data.columns:
            master_data = master_data[master_data['City'] == selected_city]
        else:
            st.sidebar.warning("City column is missing in the data.")
    else:
        master_data = master_data.drop(columns=['City'], errors='ignore') 
    
    
    appointment_letter = st.sidebar.checkbox("Appointment Letter")

    if appointment_letter:
        current_year = date.today().year
        years = list(range(current_year, 2018, -1))
        selected_years = st.sidebar.multiselect("Select Years", years, key="al_selected_years")
        if not selected_years:
            selected_years = years

        months = [
            ("01", "January"), ("02", "February"), ("03", "March"),
            ("04", "April"), ("05", "May"), ("06", "June"),
            ("07", "July"), ("08", "August"), ("09", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        month_map = {name: code for code, name in months}
        selected_month_names = st.sidebar.multiselect("Select Months", [month[1] for month in months], default=[month[1] for month in months], key="al_selected_monthes")
        selected_months = [month_map[name] for name in selected_month_names]

       
        appointment_status = st.sidebar.radio(
            "Select Appointment Status",
            options=["Issued but Signed Document Missing", "Signed Document Uploaded", "Pending"],
            key="appointment_status"
        )

        st.sidebar.markdown("---")
       
        if 'Appointment Date' in master_data.columns:
           
            master_data['Appointment Date'] = pd.to_datetime(master_data['Appointment Date'], errors='coerce')

        
            if appointment_status == "Pending":
                master_data = master_data[master_data['Appointment Date'].isna()]
                master_data = master_data.drop(columns=['Appointment Date', 'Issuing Manager name', 'Basic Salary', 'HR Name', 'HR Designation', 'Issuing Designation'], errors='ignore')
            else:
                master_data = master_data[
                    master_data['Appointment Date'].dt.year.isin(selected_years) &
                    master_data['Appointment Date'].dt.strftime('%m').isin(selected_months)
                ]
            
            if appointment_status and 'Appointment Letter' in master_data.columns:
                master_data = master_data[master_data['Appointment Letter'] == appointment_status]
            elif 'Appointment Letter' not in master_data.columns:
                st.sidebar.warning("Appointment Letter column is missing in the data.")
    else:
        master_data = master_data.drop(columns=['Appointment Date', 'Appointment Letter'], errors='ignore')
        master_data = master_data.drop(columns=['Issuing Manager name', 'Basic Salary', 'HR Name', 'HR Designation', 'Issuing Designation'], errors='ignore')



  # Sidebar Probation Confirmation Checkbox
    probation_confirmation = st.sidebar.checkbox("Probation Confirmation")

    if probation_confirmation:
        # Define current year and available years
        current_year = date.today().year
        years = list(range(current_year, 2018, -1))
        
        # Multiselect for years
        selected_years = st.sidebar.multiselect(
            "Select Years", years, default=years, key="al_selected_yearpr"
        )
        
        # Define months and map for selection
        months = [
            ("01", "January"), ("02", "February"), ("03", "March"),
            ("04", "April"), ("05", "May"), ("06", "June"),
            ("07", "July"), ("08", "August"), ("09", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        month_map = {name: code for code, name in months}
        selected_month_names = st.sidebar.multiselect(
            "Select Months", [month[1] for month in months], 
            default=[month[1] for month in months], 
            key="al_selected_monthpb"
        )
        selected_months = [month_map[name] for name in selected_month_names]
        
        # Radio button for Probation Status
        probation_status = st.sidebar.radio(
            "Select Probation Status", options=["Pending", "Confirmed"], index=0, key="pc_status"
        )
        
        st.sidebar.markdown("---")
        
       
        master_data['DateofJoining'] = pd.to_datetime(master_data['DateofJoining'], errors='coerce')
        
        
        master_data['Confirmation Date'] = master_data['DateofJoining'].apply(
            lambda x: x + relativedelta(months=6) if pd.notnull(x) else pd.NaT
        )
        
        
        master_data['Confirmation Date'] = master_data['Confirmation Date'].dt.strftime('%d %b %Y')
        master_data['DateofJoining'] = master_data['DateofJoining'].dt.strftime('%d %b %Y')
        
        if probation_status == "Confirmed":
            master_data = master_data[
                pd.to_datetime(master_data['Confirmation Date'], errors='coerce').dt.year.isin(selected_years) &
                pd.to_datetime(master_data['Confirmation Date'], errors='coerce').dt.strftime('%m').isin(selected_months)
            ]
            master_data = master_data.drop(columns=['Extended Confirmations'], errors='ignore')
        elif probation_status == "Pending":
            master_data = master_data.drop(columns=['Confirmations Date'], errors='ignore')
            master_data = master_data[
                pd.to_datetime(master_data['Confirmation Date'], errors='coerce').dt.year.isin(selected_years) &
                pd.to_datetime(master_data['Confirmation Date'], errors='coerce').dt.strftime('%m').isin(selected_months)
            ]
        
        
        master_data = master_data[
            master_data['Probation Confirmation'].str.contains(probation_status, na=False)
        ]
    else:
        # Drop columns related to Probation Confirmation if the checkbox is unchecked
        master_data = master_data.drop(
            columns=['Probation Confirmation', 'Extended Confirmations', 'Confirmations Date'], 
            errors='ignore'
        )


    letter_of_promotion = st.sidebar.checkbox("Letter of Promotion")

    if letter_of_promotion:
        current_year = date.today().year
        years = list(range(current_year, 2018, -1))
        selected_years = st.sidebar.multiselect("Select Years", years, key="lp_selected_year")
        if not selected_years:
            selected_years = years

        months = [
            ("01", "January"), ("02", "February"), ("03", "March"),
            ("04", "April"), ("05", "May"), ("06", "June"),
            ("07", "July"), ("08", "August"), ("09", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        month_map = {name: code for code, name in months}
        selected_month_names = st.sidebar.multiselect("Select Months", [month[1] for month in months], default=[month[1] for month in months], key="lp_selected_month")
        selected_months = [month_map[name] for name in selected_month_names]

       
        promotion_status = st.sidebar.radio("Select Promotion Status", options=["Issued", "Pending"], index=0, key="lp_status")
        
        st.sidebar.markdown("---")

        promotion_statuses = [promotion_status]

       
        if promotion_statuses:
            master_data = master_data[master_data['Letter of Promotion'].isin(promotion_statuses)]

        
        if 'Date of Promotion' in master_data.columns:
            master_data['Date of Promotion'] = pd.to_datetime(master_data['Date of Promotion'], errors='coerce')

            if "Pending" in promotion_statuses:  
                master_data = master_data[master_data['Date of Promotion'].isna()]
                master_data = master_data.drop(columns=['Date of Promotion', 'Promotion Designation', 'Issuing Manager Promotion', 'Issuing Designation Promotion'], errors='ignore')
            else:
                master_data = master_data[
                    master_data['Date of Promotion'].dt.year.isin(selected_years) & 
                    master_data['Date of Promotion'].dt.strftime('%m').isin(selected_months)
                ]
            
        if 'Letter of Promotion' not in master_data.columns:
            st.sidebar.warning("Letter of Promotion column is missing in the data.")
    else:
        master_data = master_data.drop(columns=['Letter of Promotion', 'Date of Promotion', 'Promotion Designation', 'Issuing Manager Promotion', 'Issuing Designation Promotion'], errors='ignore')

    resignation = st.sidebar.checkbox("Resignation")
    if resignation:
        current_year = date.today().year
        years = list(range(current_year, 2018, -1))
        selected_years = st.sidebar.multiselect("Select Years", years, key="res_selected_year")
        if not selected_years:
            selected_years = years

        months = [
            ("01", "January"), ("02", "February"), ("03", "March"),
            ("04", "April"), ("05", "May"), ("06", "June"),
            ("07", "July"), ("08", "August"), ("09", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        month_map = {name: code for code, name in months}
        selected_month_names = st.sidebar.multiselect(
            "Select Months", [month[1] for month in months], default=[month[1] for month in months], key="res_selected_month"
        )
        selected_months = [month_map[name] for name in selected_month_names]

        resignation_status = st.sidebar.radio(
            "Resignation Status", 
            options=["Approved", "Pending for Approval"],
            key="res_status"
        )
        st.sidebar.markdown("---")

        if 'Resignation Date' in master_data.columns:
            master_data['Resignation Date'] = pd.to_datetime(master_data['Resignation Date'], errors='coerce')
            
            if resignation_status == "Pending for Approval":
                master_data = master_data[master_data['Resignation Date'].isna()]
                master_data = master_data.drop(
                    columns=[
                        'Resignation Date', 'Type of Resignation', 'Notice Period ', 
                        'Reason of Resignation', 'Resignation Submitted', 
                        'Resignation Acceptance Date', 'Resignation Acceptance'
                    ], 
                    errors='ignore'
                )
            elif resignation_status == "Approved" or resignation_status == "All":
                master_data = master_data[
                    master_data['Resignation Date'].dt.year.isin(selected_years) &
                    master_data['Resignation Date'].dt.strftime('%m').isin(selected_months)
                ]

                if resignation_status != "All" and 'Resignation' in master_data.columns:
                    master_data = master_data[master_data['Resignation'] == resignation_status]
                elif 'Resignation' not in master_data.columns:
                    st.sidebar.warning("Resignation column is missing in the data.")
        else:
            st.sidebar.warning("Resignation Date column is missing in the data.")
    else:
        master_data = master_data.drop(
            columns=[
                'Resignation Date', 'Resignation', 'Type of Resignation',
                'Notice Period ', 'Reason of Resignation', 'Resignation Submitted',
                'Resignation Acceptance Date', 'Resignation Acceptance'
            ], 
            errors='ignore'
        )



    letter_of_salary_increment = st.sidebar.checkbox("Letter of Salary Increment")
    if letter_of_salary_increment:
        current_year = date.today().year
        years = list(range(current_year, 2018, -1))
        selected_years = st.sidebar.multiselect("Select Years", years, key="al_selected_yearletter")
        if not selected_years:
            selected_years = years

        months = [
            ("01", "January"), ("02", "February"), ("03", "March"),
            ("04", "April"), ("05", "May"), ("06", "June"),
            ("07", "July"), ("08", "August"), ("09", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        month_map = {name: code for code, name in months}
        selected_month_names = st.sidebar.multiselect(
            "Select Months", [month[1] for month in months], default=[month[1] for month in months], key="al_selected_monthletter"
        )
        selected_months = [month_map[name] for name in selected_month_names]

        
        salary_increment_status = st.sidebar.radio(
            "Salary Increment Status",
            options=[ "Issued", "Pending"],
           
            key="si_status"
        )
        
        if 'Salary Increment Date' in master_data.columns:
            master_data['Salary Increment Date'] = pd.to_datetime(master_data['Salary Increment Date'], errors='coerce')

           
            if salary_increment_status == "Issued":
                master_data = master_data[master_data['Salary Increment Date'].notna()]
                master_data = master_data[
                    master_data['Salary Increment Date'].dt.year.isin(selected_years) & 
                    master_data['Salary Increment Date'].dt.strftime('%m').isin(selected_months)
                ]
            elif salary_increment_status == "Pending":
                master_data = master_data[master_data['Salary Increment Date'].isna()]
                master_data = master_data.drop(columns=['Salary Increment Date','Salary Increment CTC','Issuing Manager Name','Issuing Designations' ], errors='ignore')
            
            if 'Letter of Salary Increment' not in master_data.columns:
                st.sidebar.warning("Letter of Salary Increment column is missing in the data.")
        else:
            st.sidebar.warning("Salary Increment Date column is missing in the data.")
    else:
       
        master_data = master_data.drop(
            columns=[
                'Salary Increment Date', 
                'Letter of Salary Increment','Salary Increment CTC','Issuing Manager Name','Issuing Designations'
            ], 
            errors='ignore'
        )


   
    fnf = st.sidebar.checkbox("FNF")
    if fnf:
        current_year = date.today().year
        years = list(range(current_year, 2018, -1)) 
        selected_years = st.sidebar.multiselect("Select Years", years, key="fnf_selected_yeares")
        if not selected_years:
            selected_years = years  

        months = [
            ("01", "January"), ("02", "February"), ("03", "March"),
            ("04", "April"), ("05", "May"), ("06", "June"),
            ("07", "July"), ("08", "August"), ("09", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        month_map = {name: code for code, name in months}
        selected_month_names = st.sidebar.multiselect(
            "Select Months", [month[1] for month in months], default=[month[1] for month in months], key="fnf_selected_month"
        )
        selected_months = [month_map[name] for name in selected_month_names]

        fnf_status = st.sidebar.radio("Select FNF Status", options=["Issued", "Pending"])

        st.sidebar.markdown("---")

        fnf_statuses = []
        if fnf_status == "Issued":
            fnf_statuses.append("Issued")
        elif fnf_status == "Pending":
            fnf_statuses.append("Pending")

        if 'Date of Leaving' in master_data.columns:
            master_data['Date of Leaving'] = pd.to_datetime(master_data['Date of Leaving'], errors='coerce')  
            
            if fnf_statuses:
                master_data = master_data[master_data['FNF'].isin(fnf_statuses)]  
                
                
                if fnf_status == "Issued":
                    master_data = master_data[
                        master_data['Date of Leaving'].notna() &  
                        master_data['Date of Leaving'].dt.year.isin(selected_years) &  
                        master_data['Date of Leaving'].dt.strftime('%m').isin(selected_months)  
                    ]
                
              
                elif fnf_status == "Pending":
                    master_data = master_data[master_data['Date of Leaving'].isna()]  
                    master_data = master_data.drop(columns=['Date of Leaving', 'Audited By', 'Final Status', 'Payment Status','Absconding','Resignations','Terminated','Payment paid Amount'], errors='ignore')

        else:
            st.sidebar.warning("Date of Leaving column is missing in the data.")

        if 'FNF' not in master_data.columns:
            st.sidebar.warning("FNF status column is missing in the data.")

    else:
       
        master_data = master_data.drop(columns=['FNF', 'Audited By', 'Final Status', 'Payment Status', 'Date of Leaving','Absconding','Resignations','Terminated','Payment paid Amount'], errors='ignore')


    Clearencestatusdata = st.sidebar.checkbox("Clearance Status")

    if Clearencestatusdata:
        current_year = date.today().year
        years = list(range(current_year, 2018, -1)) 
        selected_years = st.sidebar.multiselect("Select Years", years, key="cle_selected_year")
        if not selected_years:
            selected_years = years  

        months = [
            ("01", "January"), ("02", "February"), ("03", "March"),
            ("04", "April"), ("05", "May"), ("06", "June"),
            ("07", "July"), ("08", "August"), ("09", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        month_map = {name: code for code, name in months}
        selected_month_names = st.sidebar.multiselect(
            "Select Months", [month[1] for month in months], default=[month[1] for month in months], key="cle_selected_month"
        )
        selected_months = [month_map[name] for name in selected_month_names]

        clearance_status = st.sidebar.radio(
            "Select Clearance Status", 
            options=["Issued", "Pending"], 
            index=0  
        )
        st.sidebar.markdown("---")
        
       
        if 'Separation Date' in master_data.columns:
            master_data['Separation Date'] = pd.to_datetime(master_data['Separation Date'], errors='coerce')

           
            if clearance_status == "Issued":
                
                master_data = master_data[
                    master_data['Separation Date'].notna() &  
                    master_data['Separation Date'].dt.year.isin(selected_years) &  
                    master_data['Separation Date'].dt.strftime('%m').isin(selected_months)  
                ]
            
            elif clearance_status == "Pending":
                
                master_data = master_data[master_data['Separation Date'].isna()]
                
                master_data = master_data.drop(columns=['Separation Date'], errors='ignore')
            
        
        if 'Clearence Status' not in master_data.columns:
            st.sidebar.warning("Clearence Status column is missing in the data.")
    else:
        
        master_data = master_data.drop(columns=['Clearence Status', 'Separation Date'], errors='ignore')




   
    ExitInterview = st.sidebar.checkbox("Exit Interview Status")

    if ExitInterview:
       
        current_year = date.today().year
        years = list(range(current_year, 2018, -1))
        selected_years = st.sidebar.multiselect("Select Years", years, key="exit_selected_year")
        if not selected_years:
            selected_years = years  

        months = [
            ("01", "January"), ("02", "February"), ("03", "March"),
            ("04", "April"), ("05", "May"), ("06", "June"),
            ("07", "July"), ("08", "August"), ("09", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ]
        month_map = {name: code for code, name in months}
        selected_month_names = st.sidebar.multiselect(
            "Select Months", [month[1] for month in months], default=[month[1] for month in months], key="exit_selected_month"
        )
        selected_months = [month_map[name] for name in selected_month_names]
        
        
        exit_interview_status = st.sidebar.radio(
            "Select Exit Interview Status", 
            options=["Complete", "Pending"], 
            index=0 
        )
        st.sidebar.markdown("---")

        exit_interview_statuses = []
        
        if exit_interview_status == "Complete":
            exit_interview_statuses.append("Complete")
        elif exit_interview_status == "Pending":
            exit_interview_statuses.append("Pending")
        
        
        if exit_interview_statuses:
            master_data = master_data[master_data['Exit Interview Status'].isin(exit_interview_statuses)]
        
       
        if 'Leaving Date' in master_data.columns:
            master_data['Leaving Date'] = pd.to_datetime(master_data['Leaving Date'], errors='coerce')
            
            if "Complete" in exit_interview_statuses:
                
                master_data = master_data[
                    master_data['Leaving Date'].notna() &  
                    master_data['Leaving Date'].dt.year.isin(selected_years) &  
                    master_data['Leaving Date'].dt.strftime('%m').isin(selected_months)
                ]
            
        
        if 'Exit Interview Status' not in master_data.columns:
            st.sidebar.warning("Exit Interview Status column is missing in the data.")
        
        
        if exit_interview_status == "Pending":
            master_data = master_data.drop(columns=['Leaving Date', 'Reason Leaving', 'Notice period'], errors='ignore')

    else:
        
        master_data = master_data.drop(columns=['Exit Interview Status', 'Leaving Date', 'Reason Leaving', 'Notice period'], errors='ignore')


    st.title("Master Report")
    if master_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        df_display = master_data.drop(columns=['EmpID', 'work_departmentorg_id'])
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        
        
        st.dataframe(df_display, width=1400, column_config={"View": st.column_config.LinkColumn("View", display_text="View")})
        excel_data = convert_df_to_excel(master_data)
        pdf_data = create_pdf_report(master_data, "Master Report", selected_org)

        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.download_button(label="📥Download Excel", data=excel_data, file_name='master_data.xlsx', 
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with col2:
            st.download_button(label="📥Download PDF", data=pdf_data, file_name='master_data.pdf', 
                               mime='application/pdf')
  
    
   

    


  

  

elif selected_report == "Other Report":
    st.sidebar.title("Filters for Other Report")
    st.sidebar.text("Custom filters for other reports will appear here.")




import pandas as pd

import streamlit as st
import pandas as pd
from django.db.models import OuterRef, Subquery, F, Value
from django.db.models.functions import Concat

def fetch_EmployeesHistory_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        
        employees = EmployeePersonalDetails.objects.annotate(
            work_division=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Division')[:1]),
            work_designation=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Designation')[:1]),
            work_department=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Department')[:1]),
            Level=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Level')[:1]),

            ReportingtoDepartment=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('ReportingtoDepartment')[:1]),

            ReportingtoDesignation=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('ReportingtoDesignation')[:1]),

            work_date_of_joining=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('DateofJoining')[:1]),
            work_status=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('EmpStatus')[:1])
        ).filter(IsDelete=False, OrganizationID=org_id)

        if filters.get("EmployeeCode"):
            employees = employees.filter(EmployeeCode__icontains=filters["EmployeeCode"])
        
        if filters.get("FirstName"):
            employees = employees.filter(FirstName__icontains=filters["FirstName"])

        employees = employees.annotate(
            full_name=Concat(
                F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
            )
        )

        employee_df = pd.DataFrame(list(employees.values(
            'full_name', 'EmployeeCode', 'work_division', 'work_department', 'work_designation','ReportingtoDesignation', 
            'work_date_of_joining', 'work_status'
        )))

        # Handle the 'work_date_of_joining' column if it exists
        if 'work_date_of_joining' in employee_df.columns:
            employee_df['work_date_of_joining'] = pd.to_datetime(
                employee_df['work_date_of_joining'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            employee_df['work_date_of_joining'] = 'N/A'

        employee_df = employee_df.rename(columns={
            'full_name': 'Employee Name',
            'EmployeeCode': 'Employee Code', 
            'work_division': 'Division',
            'work_department': 'Department',
            'work_designation': 'Designation',
            # 'ReportingtoDepartment': 'Reporting Department',
            'ReportingtoDesignation': 'Reporting To Designation',
            'work_date_of_joining': 'Date of Joining',
            'work_status': 'Status'
        })
        return employee_df

    return pd.DataFrame()



# New Added Function for Locker Allotment Report
def fetch_Locker_Allotment_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    print("new report type is here:: --  :", report_type)
    if report_type == "Locker Allotment Report":
        print("inside Locker Allotment Report:: --  :")
        
        employees = EmployeePersonalDetails.objects.annotate(
            work_division=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Division')[:1]),

            Locker_Number=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('LockerNumber')[:1]),

            Locker_Type=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('LockerType')[:1]),

            Locker=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Locker')[:1]),


            work_designation=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Designation')[:1]),
            work_department=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Department')[:1]),
            Level=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('Level')[:1]),

            ReportingtoDepartment=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('ReportingtoDepartment')[:1]),

            ReportingtoDesignation=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('ReportingtoDesignation')[:1]),

            work_date_of_joining=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('DateofJoining')[:1]),
            work_status=Subquery(EmployeeWorkDetails.objects.filter(
                EmpID=OuterRef('EmpID'),
                IsDelete=False,
                OrganizationID=org_id
            ).values('EmpStatus')[:1])
        ).filter(IsDelete=False, OrganizationID=org_id)

        if filters.get("EmployeeCode"):
            employees = employees.filter(EmployeeCode__icontains=filters["EmployeeCode"])
        
        if filters.get("FirstName"):
            employees = employees.filter(FirstName__icontains=filters["FirstName"])

        employees = employees.annotate(
            full_name=Concat(
                F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
            )
        )

        employee_df = pd.DataFrame(list(employees.values(
            'full_name', 'EmployeeCode', 'work_division', 'work_department', 'work_designation', 'Locker', 'Locker_Number', 'Locker_Type','ReportingtoDesignation', 
            'work_date_of_joining', 'work_status'
        )))

        # Handle the 'work_date_of_joining' column if it exists
        if 'work_date_of_joining' in employee_df.columns:
            employee_df['work_date_of_joining'] = pd.to_datetime(
                employee_df['work_date_of_joining'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            employee_df['work_date_of_joining'] = 'N/A'

        employee_df = employee_df.rename(columns={
            'full_name': 'Employee Name',
            'EmployeeCode': 'Employee Code', 
            'work_division': 'Division',
            'work_department': 'Department',
            'work_designation': 'Designation',
            # 'ReportingtoDepartment': 'Reporting Department',
            'Locker': 'Locker',
            'Locker_Number': 'Locker Number',
            'Locker_Type': 'Locker Type',
            'ReportingtoDesignation': 'Reporting To Designation',
            'work_date_of_joining': 'Date of Joining',
            'work_status': 'Status'
        })
        return employee_df

    return pd.DataFrame()



def fetch_letter_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        
        letter = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

       
        if filters.get("emp_code"):
            letter = letter.filter(emp_code__icontains=filters["emp_code"])

        if filters.get("first_name"):
            letter = letter.filter(first_name__icontains=filters["first_name"])

        
        letter_df = pd.DataFrame(list(letter.values(
             'first_name', 'date_of_appointment', 'Reporting_to_designation', 'level',
            'basic_salary', 'Hr_Name', 'Hr_Designation', 'Issuing_manager_name', 
            'Issuing_designation'
        )))
        if 'date_of_appointment' in letter_df.columns:
            letter_df['date_of_appointment'] = pd.to_datetime(
                letter_df['date_of_appointment'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            letter_df['date_of_appointment'] = 'N/A'
        letter_df = letter_df.rename(columns={
            
            'first_name': 'Employee Name',
            'date_of_appointment': 'Date of Appointment',
            'Reporting_to_designation': 'Reporting Designation',
            'level': 'Level',
            'basic_salary': 'Basic Salary',
            'Hr_Name': 'HR Name',
            'Hr_Designation': 'HR Designation',
            'Issuing_manager_name': 'Issuing Manager Name',
            'Issuing_designation': 'Issuing Designation'
        })
        return letter_df

    return pd.DataFrame()

def fetch_proconfirmation_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        confirmations = Emp_Confirmation_Master.objects.filter(
            OrganizationID=org_id,
            IsDelete=False,
        )

       
        if filters.get("EmpCode"):
            confirmations = confirmations.filter(EmpCode__icontains=filters["EmpCode"])

        if filters.get("EmpName"):
            confirmations = confirmations.filter(EmpName__icontains=filters["EmpName"])

       
        confirmation_df = pd.DataFrame(list(confirmations.values(
            'EmpName', 'Position', 'JoiningDate', 'ConfDate', 
            'EmpConfirm', 'Extended', 'Strengths', 'Improvement', 'Guidelines', 
            'Trainingattended'
        )))

        if 'JoiningDate' in confirmation_df.columns:
            confirmation_df['JoiningDate'] = pd.to_datetime(
                confirmation_df['JoiningDate'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            confirmation_df['JoiningDate'] = 'N/A'

        # Safe formatting of 'ConfDate'
        if 'ConfDate' in confirmation_df.columns:
            confirmation_df['ConfDate'] = pd.to_datetime(
                confirmation_df['ConfDate'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            confirmation_df['ConfDate'] = 'N/A'
        confirmation_df = confirmation_df.rename(columns={
            'EmpName': 'Employee Name',
            'Position': 'Position',
            'JoiningDate': 'Joining Date',
            'ConfDate': 'Confirmation Date',
            'EmpConfirm': 'Employee Confirmed',
            'Extended': 'Extension Status',
            'Strengths': 'Strengths',
            'Improvement': 'Improvement Areas',
            'Guidelines': 'Guidelines Followed',
            'Trainingattended': 'Training Attended'
        })

        
        boolean_columns = ['Employee Confirmed', 'Extension Status', 'Guidelines Followed']

        
        for col in boolean_columns:
            if col in confirmation_df.columns:
                confirmation_df[col] = confirmation_df[col].apply(lambda x: 'Yes' if x else 'No')

        return confirmation_df

    return pd.DataFrame()





from LetterOfConfirmation.models import LETTEROFCONFIRMATIONEmployeeDetail
def fetch_confirmation_letter_data(report_type, org_id, report_options, filters):
    
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
       
        confirmation_letters = LETTEROFCONFIRMATIONEmployeeDetail.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

        
        if filters.get("emp_code"):
            confirmation_letters = confirmation_letters.filter(emp_code__icontains=filters["emp_code"])

        if filters.get("first_name"):
            confirmation_letters = confirmation_letters.filter(first_name__icontains=filters["first_name"])

     

        
        confirmation_letter_df = pd.DataFrame(list(confirmation_letters.values(
            'first_name',  'date_of_appointment',
            'date_of_confirmation',  'designation',
            
        )))

            # Safe formatting of 'date_of_appointment'
        if 'date_of_appointment' in confirmation_letter_df.columns:
            confirmation_letter_df['date_of_appointment'] = pd.to_datetime(
                confirmation_letter_df['date_of_appointment'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            confirmation_letter_df['date_of_appointment'] = 'N/A'

        # Safe formatting of 'date_of_confirmation'
        if 'date_of_confirmation' in confirmation_letter_df.columns:
            confirmation_letter_df['date_of_confirmation'] = pd.to_datetime(
                confirmation_letter_df['date_of_confirmation'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            confirmation_letter_df['date_of_confirmation'] = 'N/A'

        confirmation_letter_df = confirmation_letter_df.rename(columns={
           
            'first_name': 'Employee Name',
            
            'date_of_appointment': 'Appointment Date',
            'date_of_confirmation': 'Confirmation Date',
            
            'designation': 'Designation',
          
        })

        return confirmation_letter_df

    return pd.DataFrame()








def fetch_salary_increment_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
      
        salary_increments = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

        
        if filters.get("emp_code"):
            salary_increments = salary_increments.filter(emp_code__icontains=filters["emp_code"])

        if filters.get("first_name"):
            salary_increments = salary_increments.filter(first_name__icontains=filters["first_name"])

      

        
        salary_increment_df = pd.DataFrame(list(salary_increments.values(
              'first_name',  'date_of_salary_increament', 
             'designation', 'CTC', 'Issuing_manager_name', 'Issuing_designation', 
            
        )))
                # Safe formatting of 'date_of_salary_increament'
        if 'date_of_salary_increament' in salary_increment_df.columns:
            salary_increment_df['date_of_salary_increament'] = pd.to_datetime(
                salary_increment_df['date_of_salary_increament'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            salary_increment_df['date_of_salary_increament'] = 'N/A'

        salary_increment_df = salary_increment_df.rename(columns={
           
            'first_name': 'Employee Name',
            'date_of_salary_increament': 'Salary Increment Date',
            
            'designation': 'Designation',
            'CTC': 'CTC Amount',
            'Issuing_manager_name': 'Issuing Manager Name',
            'Issuing_designation': 'Issuing Designation'
        })
        return salary_increment_df

    return pd.DataFrame()


def fetch_promotion_letter_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        
        promotion_letters = PromotionLetterEmployeeDetail.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

       
        if filters.get("emp_code"):
            promotion_letters = promotion_letters.filter(emp_code__icontains=filters["emp_code"])

        if filters.get("first_name"):
            promotion_letters = promotion_letters.filter(first_name__icontains=filters["first_name"])

       
        
        promotion_letter_df = pd.DataFrame(list(promotion_letters.values(
             'first_name',  'date_of_promtion', 
             'designation', 'Promotiondesignation', 'Issuing_manager_name', 
            'Issuing_designation', 
        )))
        if 'date_of_promtion' in promotion_letter_df.columns:
            promotion_letter_df['date_of_promtion'] = pd.to_datetime(
                promotion_letter_df['date_of_promtion'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            promotion_letter_df['date_of_promotion'] = 'N/A'
        promotion_letter_df = promotion_letter_df.rename(columns={
           
            'first_name': 'Employee Name',
           
            'date_of_promtion': 'Promotion Date',
           
            'designation': 'Current Designation',
            'Promotiondesignation': 'Promoted Designation',
            'Issuing_manager_name': 'Issuing Manager Name',
            'Issuing_designation': 'Issuing Designation'
        })

        return promotion_letter_df

    return pd.DataFrame()

import pandas as pd

import pandas as pd
from Warning_Letters.models import VerbalWarningmoduls, WrittenWarningModul, FinalWarningModule

def fetch_all_warning_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        verbal_warnings = VerbalWarningmoduls.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )
        written_warnings = WrittenWarningModul.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )
        final_warnings = FinalWarningModule.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

        if filters:
            if filters.get("emp_code"):
                verbal_warnings = verbal_warnings.filter(emp_code__icontains=filters["emp_code"])
                written_warnings = written_warnings.filter(employee_no__icontains=filters["emp_code"])
                final_warnings = final_warnings.filter(employee_no__icontains=filters["emp_code"])

            if filters.get("emp_name"):
                verbal_warnings = verbal_warnings.filter(emp_name__icontains=filters["emp_name"])
                written_warnings = written_warnings.filter(name__icontains=filters["emp_name"])
                final_warnings = final_warnings.filter(name__icontains=filters["emp_name"])

        # Verbal Warnings DataFrame
        verbal_column_names = {
            'emp_name': 'Employee Name',
            'designation': 'Employee Designation',
            'problems': 'Problems',
            'improvements': 'Improvements',
            'from_date': 'From Date',
            'to_date': 'To Date',
            'time': 'Time',
            'venue': 'Venue',
            'verbally_warned': 'Verbally Warned',
            'appeal_explained': 'Appeal Explained',
            'appeal': 'Appeal',
            'reviewed_by': 'Reviewed By',
            'associate_signature_date': 'Associate Signature Date',
            'manager_signature_date': 'Manager Signature Date'
        }

        verbal_warning_df = pd.DataFrame(list(verbal_warnings.values(
            'emp_name', 'designation', 'problems', 'improvements', 
            'from_date', 'to_date', 'time', 'venue', 'verbally_warned', 'appeal_explained',
            'appeal', 'reviewed_by', 'associate_signature_date', 'manager_signature_date'
        )))
        if 'from_date' in verbal_warning_df.columns:
            verbal_warning_df['from_date'] = pd.to_datetime(verbal_warning_df['from_date'], errors='coerce') \
                .dt.strftime('%d %b %Y').fillna('N/A')
        else:
            verbal_warning_df['from_date'] = 'N/A'

        if 'to_date' in verbal_warning_df.columns:
            verbal_warning_df['to_date'] = pd.to_datetime(verbal_warning_df['to_date'], errors='coerce') \
                .dt.strftime('%d %b %Y').fillna('N/A')
        else:
            verbal_warning_df['to_date'] = 'N/A'
        if not verbal_warning_df.empty:
            verbal_warning_df.rename(columns=verbal_column_names, inplace=True)
            verbal_warning_df.insert(2, 'Warning Type', 'Verbal')

       
        written_column_names = {
            'name': 'Employee Name',
            'designation': 'Employee Designation',
            'warnings': 'Warnings',
            'problems': 'Problems',
            'written_warning': 'Written Warning',
            'improvements': 'Improvements',
            'supervisor_signature_date': 'Supervisor Signature Date',
            'associate_signature_date': 'Associate Signature Date',
            'reviewed_by': 'Reviewed By',
            'seen_by': 'Seen By',
            'DepartmentManager': 'Department Manager',
            'hr_manager_signature_date': 'HR Manager Signature Date'
        }

        written_warning_df = pd.DataFrame(list(written_warnings.values(
            'name', 'designation', 'warnings', 'problems', 
            'written_warning', 'improvements', 
            'supervisor_signature_date', 'associate_signature_date', 'reviewed_by', 'seen_by', 
            'DepartmentManager', 'hr_manager_signature_date'
        )))
        if 'supervisor_signature_date' in written_warning_df.columns:
            written_warning_df['supervisor_signature_date'] = pd.to_datetime(
                written_warning_df['supervisor_signature_date'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            written_warning_df['supervisor_signature_date'] = 'N/A'

        if 'associate_signature_date' in written_warning_df.columns:
            written_warning_df['associate_signature_date'] = pd.to_datetime(
                written_warning_df['associate_signature_date'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            written_warning_df['associate_signature_date'] = 'N/A'

        if 'hr_manager_signature_date' in written_warning_df.columns:
            written_warning_df['hr_manager_signature_date'] = pd.to_datetime(
                written_warning_df['hr_manager_signature_date'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            written_warning_df['hr_manager_signature_date'] = 'N/A'
        if not written_warning_df.empty:
            written_warning_df.rename(columns=written_column_names, inplace=True)
            written_warning_df.insert(2, 'Warning Type', 'Written')

       
        final_column_names = {
            'name': 'Employee Name',
            'designation': 'Employee Designation',
            'warning_type': 'Warning Type',
            'employee_problem': 'Employee Problem',
            'written_warning': 'Written Warning',
            'improvement_standard': 'Improvement Standard',
            'supervisor_signature_date': 'Supervisor Signature Date',
            'associate_signature_date': 'Associate Signature Date',
            'reviewed_by': 'Reviewed By',
            'department_signature_date': 'Department Signature Date',
            'hr_manager_signature': 'HR Manager Signature'
        }

        final_warning_df = pd.DataFrame(list(final_warnings.values(
            'name', 'designation', 'employee_problem', 
            'written_warning', 'improvement_standard', 
            'supervisor_signature_date', 'associate_signature_date', 'reviewed_by', 
            'department_signature_date', 'hr_manager_signature'
        )))
        if 'supervisor_signature_date' in final_warning_df.columns:
            final_warning_df['supervisor_signature_date'] = pd.to_datetime(
                final_warning_df['supervisor_signature_date'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            final_warning_df['supervisor_signature_date'] = 'N/A'

        if 'associate_signature_date' in final_warning_df.columns:
            final_warning_df['associate_signature_date'] = pd.to_datetime(
                final_warning_df['associate_signature_date'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            final_warning_df['associate_signature_date'] = 'N/A'

        if 'department_signature_date' in final_warning_df.columns:
            final_warning_df['department_signature_date'] = pd.to_datetime(
                final_warning_df['department_signature_date'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            final_warning_df['department_signature_date'] = 'N/A'
        if not final_warning_df.empty:
            final_warning_df.rename(columns=final_column_names, inplace=True)
            final_warning_df.insert(2, 'Warning Type', 'Final')

        return verbal_warning_df, written_warning_df, final_warning_df

    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


def fetch_resignation_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
       
        resignations = EmpResigantionModel.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

        
        if filters.get("Emp_Code"):
            resignations = resignations.filter(Emp_Code__icontains=filters["Emp_Code"])

        if filters.get("Name"):
            resignations = resignations.filter(Name__icontains=filters["Name"])

       
        resignation_df = pd.DataFrame(list(resignations.values(
            'Name',  'Designation', 'TypeofRes',
            'NoticePeriod', 'Res_Reason', 'Ressubmittedto', 'LastWorkingDays', 
            'Res_acceptance_Date', 'Res_acceptance_By'
        )))
            # Handle 'Res_acceptance_Date'
        if 'Res_acceptance_Date' in resignation_df.columns:
            resignation_df['Res_acceptance_Date'] = pd.to_datetime(
                resignation_df['Res_acceptance_Date'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            resignation_df['Res_acceptance_Date'] = 'N/A'

        # Handle 'LastWorkingDays'
        if 'LastWorkingDays' in resignation_df.columns:
            resignation_df['LastWorkingDays'] = pd.to_datetime(
                resignation_df['LastWorkingDays'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            resignation_df['LastWorkingDays'] = 'N/A'

        resignation_df = resignation_df.rename(columns={
                
                'Name': 'Employee Name',
               
                'Designation': 'Current Designation',
                'TypeofRes': 'Type of Resignation',
                'NoticePeriod': 'Notice Period',
                'Res_Reason': 'Reason for Resignation',
                'Ressubmittedto': 'Resignation Submitted To',
                'LastWorkingDays': 'Last Working Day',
                'Res_acceptance_Date': 'Resignation Acceptance Date',
                'Res_acceptance_By': 'Accepted By'
            })
        return resignation_df

    return pd.DataFrame()

def fetch_exitinterview_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

     
    if report_type == "Employees History":
        
        exit_interviews = Exitinterviewdata.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

        
        if filters.get("Employee_Code"):
            exit_interviews = exit_interviews.filter(Employee_Code__icontains=filters["Employee_Code"])
        
        if filters.get("EmpName"):
            exit_interviews = exit_interviews.filter(EmpName__icontains=filters["EmpName"])

        
        exit_interview_df = pd.DataFrame(list(exit_interviews.values(
             'EmpName', 'Job_Title', 'DateofJoining', 
            'DateofLeaving', 'NoticePeriod', 'ReasonForLeaving', 
            'Resign', 'Termination','FinalComment', 
        )))
        if 'DateofJoining' in exit_interview_df.columns:
            exit_interview_df['DateofJoining'] = pd.to_datetime(
                exit_interview_df['DateofJoining'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            exit_interview_df['DateofJoining'] = 'N/A'

        # Handle 'DateofLeaving'
        if 'DateofLeaving' in exit_interview_df.columns:
            exit_interview_df['DateofLeaving'] = pd.to_datetime(
                exit_interview_df['DateofLeaving'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            exit_interview_df['DateofLeaving'] = 'N/A'
        exit_interview_df = exit_interview_df.rename(columns={
            'EmpName':'Employee Name',
            'Job_Title': 'Designation',
            'DateofJoining':'Date of Joining',
            'DateofLeaving':'Date of Leaving',
            'NoticePeriod':'Notice Period',
            'ReasonForLeaving':'Reason For Leaving',
            'FinalComment':'Final Comment',
            
        })

        return exit_interview_df

    return pd.DataFrame()


def fetch_fnf_data(report_type, org_id, report_options, filters):
   
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        fnf_records = Full_and_Final_Settltment.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

        
        if filters.get("emp_code"):
            fnf_records = fnf_records.filter(Emp_Code__icontains=filters["emp_code"])

        if filters.get("Name"):
            fnf_records = fnf_records.filter(Name__icontains=filters["Name"])

    

        
        fnf_data_df = pd.DataFrame(list(fnf_records.values(
            'Name',  'DOJ', 'Date_Of_Leaving',  'Designation','Absconding','Resignation','FFPS_Payable_Amount',
            'PaymentStatus', 'PaymentPaidAmount', 'FinalStatus','AuditedBy', 'FinalStatusUpdateDate'
        )))
    
                # Handle 'DOJ'
        if 'DOJ' in fnf_data_df.columns:
            fnf_data_df['DOJ'] = pd.to_datetime(
                fnf_data_df['DOJ'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            fnf_data_df['DOJ'] = 'N/A'

        # Handle 'Date_Of_Leaving'
        if 'Date_Of_Leaving' in fnf_data_df.columns:
            fnf_data_df['Date_Of_Leaving'] = pd.to_datetime(
                fnf_data_df['Date_Of_Leaving'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            fnf_data_df['Date_Of_Leaving'] = 'N/A'

        # Handle 'FinalStatusUpdateDate'
        if 'FinalStatusUpdateDate' in fnf_data_df.columns:
            fnf_data_df['FinalStatusUpdateDate'] = pd.to_datetime(
                fnf_data_df['FinalStatusUpdateDate'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            fnf_data_df['FinalStatusUpdateDate'] = 'N/A'

        fnf_data_df = fnf_data_df.rename(columns={
            'Name': 'Employee Name',
           
            'DOJ': 'Date of Joining',
            'Date_Of_Leaving': 'Date of Leaving',
           
            'Designation': 'Designation',
            'Absconding':'Absconding',
            'Resignation':'Resignation',
            'FFPS_Payable_Amount': 'Payable Amount',
            'PaymentStatus': 'Payment Status',
            'PaymentPaidAmount': 'Paid Amount',
            'FinalStatus': 'Final Settlement Status',
            'AuditedBy':'AuditedBy',
            'FinalStatusUpdateDate': 'Settlement Status Update Date',
        })

        return fnf_data_df
        

from Clearance_From.models import ClearenceEmp,ClearanceItemDetail
def fetch_clearance_data(report_type, org_id, report_options, filters):
   
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        clearance_employees = ClearenceEmp.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

    
        if filters.get("EmpCode"):
            clearance_employees = clearance_employees.filter(EmpCode__icontains=filters["EmpCode"])

        if filters.get("Name"):
            clearance_employees = clearance_employees.filter(Name__icontains=filters["Name"])

    

        
        clearance_df = pd.DataFrame(list(clearance_employees.values(
            'Name',  'Position', 'SeparationDate', 'FinishingTime',
        )))
        if 'SeparationDate' in clearance_df.columns:
            clearance_df['SeparationDate'] = pd.to_datetime(
                clearance_df['SeparationDate'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
        else:
            clearance_df['SeparationDate'] = 'N/A'
        clearance_df = clearance_df.rename(columns={
            'Name': 'Employee Name',
            'Position':'Designation',
            'SeparationDate':'Separation Date',
            'FinishingTime':'Finishing Time',
           
          
        })
       

        return clearance_df
    

from IT.models import ItInformation,SimDetail,MobileDetail,EmailDetail,SystemDetail    

def fetch_empit_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        its = ItInformation.objects.filter(OrganizationID=org_id, IsDelete=False).order_by('-id')
        its_with_issued_status = []

        def map_status(value):
            return "Approved" if value == '1' else "Pending"

        for it in its:
           
            if filters.get("EmployeeCode") and filters["EmployeeCode"].lower() not in it.EmployeeCode.lower():
                continue
            if filters.get("EmployeeName") and filters["EmployeeName"].lower() not in it.EmployeeName.lower():
                continue

            sim_issued = SimDetail.objects.filter(ItInformation=it, IsIssued=True, OrganizationID=org_id, IsDelete=False)
            mobile_issued = MobileDetail.objects.filter(ItInformation=it, IsIssued=True, OrganizationID=org_id, IsDelete=False)
            email_issued = EmailDetail.objects.filter(ItInformation=it, IsIssued=True, OrganizationID=org_id, IsDelete=False)
            system_issued = SystemDetail.objects.filter(ItInformation=it, IsIssued=True, OrganizationID=org_id, IsDelete=False)
            its_with_issued_status.append({
                'Employee Name': it.EmployeeName,
                'Employee Code': it.EmployeeCode if it.EmployeeCode else '',
                'Designation Grade': it.DesignationGrade,
                'HR Status': map_status(it.HrStatus),
                'HR Comment': it.HrComment,
                'IT Status': map_status(it.ItStatus),
                'IT Comment': it.ItComment,
                'HOD Status': map_status(it.HodStatus),
                'HOD Comment': it.HodComment,
                'Reporting To Designation': it.ReportingtoDesigantion,
                'SIM Issued': 'Issued' if sim_issued else 'Not Issued',
                'Mobile Issued': 'Issued' if mobile_issued else 'Not Issued',
                'Email Issued': 'Issued' if email_issued else 'Not Issued',
                'System Issued': 'Issued' if system_issued else 'Not Issued',
            })

        itemp_df = pd.DataFrame(its_with_issued_status)

       

        sim_df = pd.DataFrame(list(SimDetail.objects.filter(OrganizationID=org_id, IsDelete=False)
                                   .filter(ItInformation__in=its)  
                                   .filter(ItInformation__EmployeeCode__icontains=filters.get("EmployeeCode", ""))
                                   .filter(ItInformation__EmployeeName__icontains=filters.get("EmployeeName", ""))
                                   .values('MobileNo', 'DateofRequest', 'DateofIssue', 'RequestedBy', 'IsIssued')))
        sim_df.rename(columns={
            'MobileNo': 'SIM Number',
            'DateofRequest': 'Request Date',
            'DateofIssue': 'Issue Date',
            'RequestedBy': 'Requested By',
            'IsIssued': 'Issued Status'
        }, inplace=True)

        
        if 'Request Date' in sim_df.columns:
            sim_df['Request Date'] = pd.to_datetime(sim_df['Request Date'], errors='coerce')

        if 'Issue Date' in sim_df.columns:
            sim_df['Issue Date'] = pd.to_datetime(sim_df['Issue Date'], errors='coerce')

        
        if 'Request Date' in sim_df.columns:
            sim_df['Request Date'] = sim_df['Request Date'].apply(
                lambda x: x.strftime('%d %b %Y') if pd.notnull(x) else ''
            )

        if 'Issue Date' in sim_df.columns:
            sim_df['Issue Date'] = sim_df['Issue Date'].apply(
                lambda x: x.strftime('%d %b %Y') if pd.notnull(x) else ''
            )

        sim_df['Detail Type'] = 'SIM Details'


        mobile_df = pd.DataFrame(list(MobileDetail.objects.filter(OrganizationID=org_id, IsDelete=False)
                                      .filter(ItInformation__in=its)
                                      .filter(ItInformation__EmployeeCode__icontains=filters.get("EmployeeCode", ""))
                                      .filter(ItInformation__EmployeeName__icontains=filters.get("EmployeeName", ""))
                                      .values('CompanyName', 'ModelNumber', 'IMEINumber', 'Colour', 'RequestedBy', 'IsIssued')))
        mobile_df.rename(columns={
            'CompanyName': 'Company',
            'ModelNumber': 'Model',
            'IMEINumber': 'IMEI Number',
            'Colour': 'Color',
            'RequestedBy': 'Requested By',
            'IsIssued': 'Issued Status'
        }, inplace=True)

        mobile_df['Detail Type'] = 'Mobile Details'

        email_df = pd.DataFrame(list(EmailDetail.objects.filter(OrganizationID=org_id, IsDelete=False)
                                     .filter(ItInformation__in=its)
                                     .filter(ItInformation__EmployeeCode__icontains=filters.get("EmployeeCode", ""))
                                     .filter(ItInformation__EmployeeName__icontains=filters.get("EmployeeName", ""))
                                     .values('Email', 'Type', 'DomainType', 'RequestedBy', 'IsIssued')))
        email_df.rename(columns={
            'Email': 'Email Address',
            'Type': 'Email Type',
            'DomainType': 'Domain Type',
            'RequestedBy': 'Requested By',
            'IsIssued': 'Issued Status'
        }, inplace=True)
        email_df['Detail Type'] = 'Email Details'

        system_df = pd.DataFrame(list(SystemDetail.objects.filter(OrganizationID=org_id, IsDelete=False)
                                      .filter(ItInformation__in=its)
                                      .filter(ItInformation__EmployeeCode__icontains=filters.get("EmployeeCode", ""))
                                      .filter(ItInformation__EmployeeName__icontains=filters.get("EmployeeName", ""))
                                      .values('SystemType', 'CompanyName', 'ModelNumber', 'SerialNumber', 'Configuration', 'RequestedBy', 'IsIssued')))
        system_df.rename(columns={
            'SystemType': 'System Type',
            'CompanyName': 'Company',
            'ModelNumber': 'Model',
            'SerialNumber': 'Serial Number',
            'Configuration': 'Configuration Details',
            'RequestedBy': 'Requested By',
            'IsIssued': 'Issued Status'
        }, inplace=True)
        system_df['Detail Type'] = 'System Details'

        return itemp_df, sim_df, mobile_df, email_df, system_df


from UniformInventory.models import UniformInformation,UniformDetails
def fetch_uniform_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
       
        uniform_employees = UniformInformation.objects.filter(OrganizationID=org_id, IsDelete=False)
        
        if filters.get("EmployeeCode"):
            uniform_employees = uniform_employees.filter(EmployeeCode__icontains=filters["EmployeeCode"])
        if filters.get("EmployeeName"):
            uniform_employees = uniform_employees.filter(EmployeeName__icontains=filters["EmployeeName"])

        
        employee_ids = uniform_employees.values_list('id', flat=True)

      
        uniform_details = UniformDetails.objects.filter(
            OrganizationID=org_id,
            UniformInformation__id__in=employee_ids,
            IsDelete=False
        ).select_related('UniformItemMaster')

       
        uniform_data = list(uniform_employees.values(
            'EmployeeName', 'DesignationGrade', 'HrStatus', 'HrComment',
            'HousekeppingStatus', 'HousekeppingComment', 'HodStatus', 'HodComment',
            'ReportingtoDesigantion', 'Return', 'ReturnAmount'
        ))

        
        uniform_df = pd.DataFrame(uniform_data)

       
        uniform_df.rename(columns={
            'EmployeeName': 'Employee Name',
            'DesignationGrade': 'Designation',
            'HrStatus': 'Hr Status',
            'HrComment': 'Hr Comment',
            'HousekeppingStatus': 'Housekepping Status',
            'HousekeppingComment': 'Housekepping Comment',
            'HodStatus': 'Hod Status',
            'HodComment': 'Hod Comment',
            'ReportingtoDesigantion': 'Reporting to Designation',
            'Return': 'Return',
            'ReturnAmount': 'Return Amount',
        }, inplace=True)
        
       
        uniform_detailsdata = [
            {
                "Item Name": detail_obj.UniformItemMaster.ItemName, 
                "New Qty": detail['NewQuantity'],
                "Altered Qty": detail['AlteredQuantity'],
                "Issued Qty": detail['IssuedQuantity'],
                "Return New Qty": detail['ReturnNewQuantity'],
                "Return Altered Qty": detail['ReturnAlteredQuantity'],
                "Return Issued Qty": detail['ReturnIssuedQuantity'],
                "New Variance": detail['NewVariance'],
                "Alter Variance": detail['AlterVariance'],
                "Issue Variance": detail['IssueVariance'],
                "Total Charged": detail['TotalCharged'],
            }
            for detail_obj, detail in zip(uniform_details, uniform_details.values(
                'NewQuantity', 'AlteredQuantity', 'IssuedQuantity', 'ReturnNewQuantity',
                'ReturnAlteredQuantity', 'ReturnIssuedQuantity', 'NewVariance', 'AlterVariance',
                'IssueVariance', 'TotalCharged',
            ))
        ]

        # Convert uniform_detailsdata to a DataFrame
        uniformdetails_df = pd.DataFrame(uniform_detailsdata)

        # Map 'Return' to 'Yes' or 'No' in uniform_df
        if 'Return' in uniform_df.columns:
            uniform_df['Return'] = uniform_df['Return'].apply(lambda x: 'Yes' if x == '1' else 'No')

        # Map status codes to human-readable values
        def map_status(value):
            return "Approved" if value == '1' else "Pending"

        # Apply mapping for status columns
        for status_col in ['Hr Status', 'Housekepping Status', 'Hod Status']:
            if status_col in uniform_df.columns:
                uniform_df[status_col] = uniform_df[status_col].apply(map_status)

        return uniform_df, uniformdetails_df
    
    return pd.DataFrame(), pd.DataFrame()


from Checklist_Issued.models import HREmployeeChecklist_Entry,HREmployeeChecklist_Details
import pandas as pd

def fetch_checklist_data(report_type, org_id, report_options, filters):
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        
        checklist_entries = HREmployeeChecklist_Entry.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

       
        if filters.get("EmpCode"):
            checklist_entries = checklist_entries.filter(EmpCode__icontains=filters["EmpCode"])
        if filters.get("Name"):
            checklist_entries = checklist_entries.filter(Name__icontains=filters["Name"])

        checklist_details = HREmployeeChecklist_Details.objects.filter(
            HREmployeeChecklist_Entry__in=checklist_entries,
            IsDelete=False
        ).select_related('HREmployeeChecklistMaster', 'HREmployeeChecklist_Entry')

        raw_data = list(checklist_details.values(
            'HREmployeeChecklist_Entry__Name',
            'HREmployeeChecklist_Entry__Department',
            'HREmployeeChecklist_Entry__Designtions',
            'HREmployeeChecklistMaster__Checklist',
            'ReceivedStatus'
        ))
        checklist_df = pd.DataFrame(raw_data)

        
        checklist_df.rename(columns={
            'HREmployeeChecklist_Entry__Name': 'Employee Name',
            'HREmployeeChecklist_Entry__Department': 'Department',
            'HREmployeeChecklist_Entry__Designtions': 'Designation',
            'HREmployeeChecklistMaster__Checklist': 'Checklist',
            'ReceivedStatus': 'Received Status'
        }, inplace=True)

        
        if 'Received Status' in checklist_df.columns:
            checklist_df['Received Status'] = checklist_df['Received Status'].map(
                lambda x: "Received" if x == '1' else "Pending"
            )
        else:
            checklist_df['Received Status'] = 'Pending'  

        if not checklist_df.empty:
            pivot_df = checklist_df.pivot_table(
                index=['Employee Name', 'Department', 'Designation'],
                columns='Checklist',
                values='Received Status',
                aggfunc='first'
            ).reset_index()

            pivot_df.columns.name = None
            pivot_df = pivot_df.reset_index(drop=True)

            return pivot_df
        else:
            return pd.DataFrame(columns=['Employee Code', 'Employee Name', 'Department', 'Designation'])

    return pd.DataFrame()

def fetch_leave_balanceHistory_report(report_type, org_id, report_options, filters):
    # Validate report_type
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        
        # Get work details from EmployeeWorkDetails
        work_details = EmployeeWorkDetails.objects.filter(
            EmpID=OuterRef('EmpID'),
            IsDelete=False,
            OrganizationID=org_id,
        )

        # Get leave balances from Emp_Leave_Balance_Master
        leave_balances = Emp_Leave_Balance_Master.objects.filter(
            IsDelete=False,
            OrganizationID=org_id
        ).annotate(
            leave_type=F('Leave_Type_Master__Type'),
            balance=F('Balance')
        )

        # Get employees' personal details
        employees = EmployeePersonalDetails.objects.annotate(
            Designation=Subquery(work_details.values('Designation')[:1]),
            DOJ=Subquery(work_details.values('DateofJoining')[:1]),
        ).filter(IsDelete=False, OrganizationID=org_id)

        # Apply filters
        if filters.get("FirstName"):
            employees = employees.filter(FirstName__icontains=filters["FirstName"])
        if filters.get("EmployeeCode"):
            employees = employees.filter(EmployeeCode__icontains=filters["EmployeeCode"])

        # Get employee data in the form of a list of dictionaries
        emp_data = list(employees.values(
            'FirstName', 'EmployeeCode',  # Ensure 'EmployeeCode' is selected
            'Designation', 'DOJ'
        ))

        # Check if 'EmployeeCode' is found in emp_data
        if not emp_data or 'EmployeeCode' not in emp_data[0]:
            # Handle the missing EmployeeCode scenario
            st.error("Employee Code not found in employee data.")
            return pd.DataFrame()  # Return an empty DataFrame or appropriate result

        # Format the DOJ (Date of Joining) field
        # Format the DOJ (Date of Joining) field to 'DD-Mon-YYYY' format
        for emp in emp_data:
            if emp['DOJ']:  # Check if DOJ is not None
                # Format the date in 'DD-Mon-YYYY' format (e.g., 29-Nov-2024)
                emp['DOJ'] = emp['DOJ'].strftime('%d-%b-%Y')

        # Get leave balance data
        leave_data = list(leave_balances.values('Emp_code', 'leave_type', 'balance'))

        # Organize leave data into a dictionary by employee code
        leave_dict = {}
        for leave in leave_data:
            emp_code = leave['Emp_code']
            leave_type = leave['leave_type']
            balance = leave['balance']
            if emp_code not in leave_dict:
                leave_dict[emp_code] = {}
            leave_dict[emp_code][leave_type] = balance

        # Merge leave balances with employee data
        for emp in emp_data:
            emp_leave_balances = leave_dict.get(emp['EmployeeCode'], {})
            emp.update(emp_leave_balances)

        # Create DataFrame from emp_data
        df = pd.DataFrame(emp_data)

        # Check the columns of the DataFrame
        print("DataFrame Columns:", df.columns)

        # Ensure 'EmployeeCode' exists in the DataFrame before proceeding
        if 'EmployeeCode' not in df.columns:
            st.error("'EmployeeCode' not found in DataFrame.")
            return pd.DataFrame()  # Return an empty DataFrame or appropriate result

        # Get all leave types
        leave_types = Leave_Type_Master.objects.filter(IsDelete=False, Is_Active=True).values_list('Type', flat=True)

        # Add columns for each leave type in the DataFrame if they are not present
        for leave_type in leave_types:
            if leave_type not in df.columns:
                df[leave_type] = 0

        # Create the pivot table
        pivot_table = pd.pivot_table(
            df,
            index=['EmployeeCode', 'FirstName', 'Designation', 'DOJ'],
            values=[leave_type for leave_type in leave_types if leave_type in df.columns],
            aggfunc='sum',
            fill_value=0
        ).reset_index()

        return pivot_table
    else:
        st.error("Invalid report type selected.")
        return pd.DataFrame() 

from EmpTermination.models import EmpTerminationModel
def fetch_Termination_data(report_type, org_id, report_options, filters):
   
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        Termination_employees = EmpTerminationModel.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

    
        if filters.get("Emp_Code"):
            Termination_employees = Termination_employees.filter(Emp_Code__icontains=filters["Emp_Code"])

        if filters.get("Name"):
            Termination_employees = Termination_employees.filter(Name__icontains=filters["Name"])

    

        
        Termination_df = pd.DataFrame(list(Termination_employees.values(
            'Name',  'DOJ', 'Date_Of_Termination', 'Designation','IsWarningIssued','LastWarningLatter','Remarks'
        )))
                # Handle 'DOJ' and 'Date_Of_Termination' columns
        if 'DOJ' in Termination_df.columns:
            Termination_df['DOJ'] = pd.to_datetime(
                Termination_df['DOJ'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')

        if 'Date_Of_Termination' in Termination_df.columns:
            Termination_df['Date_Of_Termination'] = pd.to_datetime(
                Termination_df['Date_Of_Termination'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')

        Termination_df.rename(columns={
                'Name': 'Employee Name',
                'DOJ': 'Date of Joining',
                'Date_Of_Termination': 'Date of Termination',
                'Designation': 'Job Title',
                'IsWarningIssued': 'Warning Issued',
                'LastWarningLatter': 'Last Warning Letter',
                'Remarks': 'Comments'
            }, inplace=True)

    
       

        return Termination_df

from EmpAbsconding.models import EmpAbscondingModel
def fetch_Absconding_data(report_type, org_id, report_options, filters):
   
    if report_type not in report_options:
        raise ValueError(f"Invalid report type: '{report_type}'. Please select a valid report from: {report_options}")

    if report_type == "Employees History":
        Absconding_employees = EmpAbscondingModel.objects.filter(
            OrganizationID=org_id,
            IsDelete=False
        )

    
        if filters.get("Emp_Code"):
            Absconding_employees = Absconding_employees.filter(Emp_Code__icontains=filters["Emp_Code"])

        if filters.get("Name"):
            Absconding_employees = Absconding_employees.filter(Name__icontains=filters["Name"])

    

                    
        Absconding_df = pd.DataFrame(list(Absconding_employees.values(
                'Name', 'DOJ', 'Date_Of_Absconding', 'Designation', 'Remarks'
            )))

            
        if 'DOJ' in Absconding_df.columns:
            Absconding_df['DOJ'] = pd.to_datetime(
                Absconding_df['DOJ'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')

        if 'Date_Of_Absconding' in Absconding_df.columns:
            Absconding_df['Date_Of_Absconding'] = pd.to_datetime(
                Absconding_df['Date_Of_Absconding'], errors='coerce'
            ).dt.strftime('%d %b %Y').fillna('N/A')
     
        column_names = {
                'Name': 'Employee Name',
                'DOJ': 'Date of Joining',
                'Date_Of_Absconding': 'Date of Absconding',
                'Designation': 'Designation',
                'Remarks': 'Remarks'
            }

        Absconding_df.rename(columns=column_names, inplace=True)
                

    
       

        return Absconding_df





if selected_report == "Employees History":
    st.sidebar.title("Filters for Employees History")

    
    EmpCode = st.sidebar.text_input("Employee Code", "")
    first_name = st.sidebar.text_input("Employee Name", "")

    
    filters = {
        "EmployeeCode": EmpCode,
        "FirstName": first_name,
        "Emp_Code": EmpCode,
        "Name": first_name,
        'emp_code':EmpCode,
        'EmpCode':EmpCode,
        'EmpName':first_name,
        'first_name':first_name,
        'emp_code':EmpCode,
        'Employee_Code':EmpCode,
        'emp_name':first_name,
        'EmployeeName':first_name,
        
    }

    
    employeeper_data = fetch_EmployeesHistory_data("Employees History", org_id, report_options, filters)
    Locker_Allotment_Data = fetch_Locker_Allotment_data("Locker Allotment Report", org_id, report_options, filters)


    letter_data = fetch_letter_data("Employees History", org_id, report_options, filters)
    probation_confirmationconfirmationletter=fetch_proconfirmation_data("Employees History", org_id, report_options, filters)
    promotion_letter=fetch_promotion_letter_data("Employees History", org_id, report_options, filters)
    salary_incrementletter=fetch_salary_increment_data("Employees History", org_id, report_options, filters)
    resignation_data = fetch_resignation_data("Employees History", org_id, report_options, filters)
    exitinterview_data = fetch_exitinterview_data("Employees History", org_id, report_options, filters)
    verbal_df, written_df, final_df = fetch_all_warning_data("Employees History", org_id, report_options, filters)

    confirmation_letterdata = fetch_confirmation_letter_data("Employees History", org_id, report_options, filters)
    fnfdata = fetch_fnf_data("Employees History", org_id, report_options, filters)

    clearancedata = fetch_clearance_data("Employees History", org_id, report_options, filters)
    itdata, sim_df, mobile_df, email_df, system_df = fetch_empit_data("Employees History", org_id, report_options, filters)

    uniformdata,uniformdetails_df= fetch_uniform_data("Employees History", org_id, report_options, filters)
    
    checklistmdata = fetch_checklist_data("Employees History", org_id, report_options, filters)

    Historylistmdata = fetch_leave_balanceHistory_report("Employees History", org_id, report_options, filters)

    Terminationlistmdata = fetch_Termination_data("Employees History", org_id, report_options, filters)

    Abscondinglistmdata = fetch_Absconding_data("Employees History", org_id, report_options, filters)


    
    st.markdown("<h5>Employee Details</h5>", unsafe_allow_html=True)
    if employeeper_data.empty:
        st.warning("No employee data available for the selected filters.")
    else:
        employeeper_data.reset_index(drop=True, inplace=True)
        employeeper_data.index += 1
        st.dataframe(employeeper_data, width=1400)
    
    st.markdown("<h5>Locker Allotment Report</h5>", unsafe_allow_html=True)
    if Locker_Allotment_Data.empty:
        st.warning("No locker allotment data available for the selected filters.")
    else:
        Locker_Allotment_Data.reset_index(drop=True, inplace=True)
        Locker_Allotment_Data.index += 1
        st.dataframe(Locker_Allotment_Data, width=1400)
    
   

    st.markdown("<h5>Employee File Check List Details</h5>", unsafe_allow_html=True)
    if checklistmdata.empty:
            st.warning("No Check List Details available for the selected filters.")
    else:
            checklistmdata.reset_index(drop=True, inplace=True)
            checklistmdata.index += 1
            st.dataframe(checklistmdata, width=1400) 


    st.markdown("<h5>Appointment Details</h5>", unsafe_allow_html=True)
    if letter_data.empty:
        st.warning("No appointment data available for the selected filters.")
    else:
        letter_data.reset_index(drop=True, inplace=True)
        letter_data.index += 1
        st.dataframe(letter_data, width=1400)

    


    st.markdown("<h5>Probation Confirmation Details</h5>", unsafe_allow_html=True)
    if probation_confirmationconfirmationletter.empty:
        st.warning("No Confirmation data available for the selected filters.")
    else:
        probation_confirmationconfirmationletter.reset_index(drop=True, inplace=True)
        probation_confirmationconfirmationletter.index += 1
        st.dataframe(probation_confirmationconfirmationletter, width=1400)
    


    st.markdown("<h5>Confirmation  Details</h5>", unsafe_allow_html=True)
    if confirmation_letterdata.empty:
        st.warning("No Confirmation data available for the selected filters.")
    else:
        confirmation_letterdata.reset_index(drop=True, inplace=True)
        confirmation_letterdata.index += 1
        st.dataframe(confirmation_letterdata, width=1400)

    st.markdown("<h5>Leave Balance History Details</h5>", unsafe_allow_html=True)
    if Historylistmdata.empty:
        st.warning("No Exit Interview Details available for the selected filters.")
    else:
        Historylistmdata.reset_index(drop=True, inplace=True)
        Historylistmdata.index += 1
        st.dataframe(Historylistmdata, width=1400)


    st.markdown("<h5>Promotion Details</h5>", unsafe_allow_html=True)
    if promotion_letter.empty:
        st.warning("No Promotion Details available for the selected filters.")
    else:
        promotion_letter.reset_index(drop=True, inplace=True)
        promotion_letter.index += 1
        st.dataframe(promotion_letter, width=1400)


    st.markdown("<h5>Salary Increment Details</h5>", unsafe_allow_html=True)
    if salary_incrementletter.empty:
        st.warning("No Salary Increment Details available for the selected filters.")
    else:
        salary_incrementletter.reset_index(drop=True, inplace=True)
        salary_incrementletter.index += 1
        st.dataframe(salary_incrementletter, width=1400)


   
    st.markdown("<h5>Warning Letters</h5>", unsafe_allow_html=True)
    if verbal_df.empty:
        st.warning("No Verbal Warning Letters available for the selected filters.")
    else:
        verbal_df.reset_index(drop=True, inplace=True)
        verbal_df.index += 1
        st.dataframe(verbal_df, width=1400)

   
    if written_df.empty:
        st.warning("No Written Warning Letters available for the selected filters.")
    else:
        written_df.reset_index(drop=True, inplace=True)
        written_df.index += 1
        st.dataframe(written_df, width=1400)

    
    if final_df.empty:
        st.warning("No Final Warning Letters available for the selected filters.")
    else:
        final_df.reset_index(drop=True, inplace=True)
        final_df.index += 1
        st.dataframe(final_df, width=1400)


    
    st.markdown("<h5>Termination Details</h5>", unsafe_allow_html=True)
    if Terminationlistmdata.empty:
        st.warning("No Termination Details available for the selected filters.")
    else:
        Terminationlistmdata.reset_index(drop=True, inplace=True)
        Terminationlistmdata.index += 1
        st.dataframe(Terminationlistmdata, width=1400)

    st.markdown("<h5>Absconding Details</h5>", unsafe_allow_html=True)
    if Abscondinglistmdata.empty:
        st.warning("No Absconding Details available for the selected filters.")
    else:
        Abscondinglistmdata.reset_index(drop=True, inplace=True)
        Abscondinglistmdata.index += 1
        st.dataframe(Abscondinglistmdata, width=1400)


    st.markdown("<h5>Resignation Details</h5>", unsafe_allow_html=True)
    if resignation_data.empty:
        st.warning("No resignation data available for the selected filters.")
    else:
        resignation_data.reset_index(drop=True, inplace=True)
        resignation_data.index += 1
        st.dataframe(resignation_data, width=1400)
    
   

        
       
    st.markdown("<h5>IT Data Details</h5>", unsafe_allow_html=True)

    
    if itdata.empty:
        st.warning("No IT Data Details available for the selected Employee.")
    else:
        itdata.reset_index(drop=True, inplace=True)
        itdata.index += 1  
        st.dataframe(itdata, width=1400)  

    
    st.markdown("<h6>SIM Details</h6>", unsafe_allow_html=True)

    
    if sim_df.empty:
        st.warning("No SIM Details available for the selected Employee.")
    else:
        sim_df.reset_index(drop=True, inplace=True)
        sim_df.index += 1  
        st.dataframe(sim_df, width=1400)  

   
    st.markdown("<h6>Mobile Details</h6>", unsafe_allow_html=True)

    
    if mobile_df.empty:
        st.warning("No Mobile Details available for the selected filters.")
    else:
        mobile_df.reset_index(drop=True, inplace=True)
        mobile_df.index += 1  
        st.dataframe(mobile_df, width=1400) 
    
    st.markdown("<h6>Email Details</h6>", unsafe_allow_html=True)

    
    if email_df.empty:
        st.warning("No Email Details available for the selected filters.")
    else:
        email_df.reset_index(drop=True, inplace=True)
        email_df.index += 1  
        st.dataframe(email_df, width=1400)  

    
    st.markdown("<h6>System Details</h6>", unsafe_allow_html=True)

    
    if system_df.empty:
        st.warning("No System Details available for the selected Employee.")
    else:
        system_df.reset_index(drop=True, inplace=True)
        system_df.index += 1  
        st.dataframe(system_df, width=1400)  

    st.markdown("<h5>Uniform Data Details</h5>", unsafe_allow_html=True)
    if uniformdata.empty:
        st.warning("No Uniform Data Details available for the selected filters.")
    else:
        uniformdata.reset_index(drop=True, inplace=True)
        uniformdata.index += 1
        st.dataframe(uniformdata, width=1400)    



    st.markdown("<h5>Uniform Count Details</h5>", unsafe_allow_html=True)
    if uniformdetails_df.empty:
        st.warning("No Uniform Count  Details available for the selected filters.")
    else:
        uniformdetails_df.reset_index(drop=True, inplace=True)
        uniformdetails_df.index += 1
        st.dataframe(uniformdetails_df, width=1400)    

   
   
   

    st.markdown("<h5>Clearance  Details</h5>", unsafe_allow_html=True)
    if clearancedata.empty:
        st.warning("No Clearance  Details available for the selected Employee.")
    else:
        clearancedata.reset_index(drop=True, inplace=True)
        clearancedata.index += 1
        st.dataframe(clearancedata, width=1400)    

   
    
    st.markdown("<h5>Exit Interview Details</h5>", unsafe_allow_html=True)
    if exitinterview_data.empty:
        st.warning("No Exit Interview Details available for the selected filters.")
    else:
        exitinterview_data.reset_index(drop=True, inplace=True)
        exitinterview_data.index += 1
        st.dataframe(exitinterview_data, width=1400)

    def convert_all_to_excel(dataframes, sheet_names):
        """
        Convert multiple DataFrames to a single Excel file with custom sheet names.
        :param dataframes: List of DataFrames
        :param sheet_names: List of corresponding sheet names
        :return: BytesIO object of the Excel file
        """
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for df, sheet_name in zip(dataframes, sheet_names):
                df.to_excel(writer, index=False, sheet_name=sheet_name[:31])  # Excel sheet name limit
        output.seek(0)
        return output

    # Prepare DataFrames and sheet names
    dfs = [
        employeeper_data, Locker_Allotment_Data, letter_data, probation_confirmationconfirmationletter,
        confirmation_letterdata, promotion_letter, salary_incrementletter,
        verbal_df, written_df, final_df, resignation_data, fnfdata,
        clearancedata, itdata, uniformdata, checklistmdata,
        exitinterview_data, Historylistmdata, Terminationlistmdata, Abscondinglistmdata
    ]

    sheet_names = [
        "Employee History", "Locker Allotment Report", "Letters", "Probation Confirmation",
        "Confirmation Letters", "Promotion Letters", "Salary Increment Letters",
        "Verbal Warnings", "Written Warnings", "Final Warnings",
        "Resignations", "Full and Final", "Clearance Data",
        "IT Data", "Uniform Data", "Checklist Data",
        "Exit Interviews", "Leave Balance History", "Termination Data", "Absconding Data"
    ]


    st.sidebar.markdown("<h5>Download All Data as Excel</h5>", unsafe_allow_html=True)
    st.sidebar.download_button(
        label="Download All Data as Excel",
        data=convert_all_to_excel(dfs, sheet_names),
        file_name="AllEmployeeHistory.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("<h5>Full and Final Details</h5>", unsafe_allow_html=True)
    if fnfdata.empty:
        st.warning("No FNF Details available for the selected filters.")
    else:
        fnfdata.reset_index(drop=True, inplace=True)
        fnfdata.index += 1
        st.dataframe(fnfdata, width=1400)    
    
















