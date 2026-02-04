import decimal
from http.client import HTTPException
import json
import os
import traceback
import django
from django.shortcuts import get_object_or_404
from html5lib import serialize
from jsonschema import ValidationError
from pydantic import BaseModel, Field
from requests import Request, Session
from fastapi import FastAPI, Depends, Form, Query
from fastapi.encoders import jsonable_encoder
from django.db import models
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime, timedelta
import sys
import django




VALID_TOKENS = {"ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f"}
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelopsmgmtpy.settings')
django.setup()
status_mapping = {
0: "Pending",
1: "Approved",
-1: "Rejected",
-2: "Cancelled"
}
from django.db import connection


from Leave_Management_System.models import CompOffApplication, Emp_Leave_Balance_Master, EmpMonthLevelCreditMaster, EmpMonthLevelDebitMaster, Leave_Application, Leave_Config_Details, Leave_Type_Master, Optional_Holidays
from Open_position.models import OpenPosition
from Employee_Payroll.models import Attendance_Data

from datetime import date

app = FastAPI()
from app.models import OrganizationMaster
@app.middleware("http")
def check_hotel_api_token(request: Request, call_next):
    token = request.headers.get("hotel-api-token")

    if not token:
        return HTTPException(status_code=400, detail="Missing 'hotel-api-token' header")

    if token not in VALID_TOKENS:
        return HTTPException(status_code=403, detail="Invalid 'hotel-api-token' value")

    response = call_next(request)
    return response

@app.get("/")
def read_root():
    return {"message": "Token is valid"}

@app.get("/another-endpoint")
def another_route():
    return {"message": "Another endpoint accessed with valid token"}

def get_leave_balance(OID: int, EmpCode: str):
    query = Emp_Leave_Balance_Master.objects.filter(
        Emp_code=EmpCode, OrganizationID=OID, IsDelete=False
    ).select_related('Leave_Type_Master')

    if not (query.exists)():
        raise HTTPException(status_code=404, detail="No leave balance found")

    data = (list)(query.values("Balance", "Leave_Type_Master__Type", "Leave_Type_Master__id"))

    # ✅ Rename the key
    formatted_data = [
        {"Balance": item["Balance"], "Type": item["Leave_Type_Master__Type"],"ID": item["Leave_Type_Master__id"]}
        for item in data
    ]

    return formatted_data
    #return (list)(query.values("Balance","Leave_Type_Master__Type"))  # Convert QuerySet to List



# ✅ FastAPI route
@app.get("/LeaveBalance")
def LeaveBalanceDetails(OID: int, UserID: str):
    EmployeeCode=""
    ed = EmployeeData(OrganizationID=OID, UserID=UserID)  # Fetch Employee Data
    if not ed or "EmployeeCode" not in ed[0]:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Employee code not found for the given UserID"}
        )

    EmployeeCode = ed[0]["EmployeeCode"]
    BalanceData = get_leave_balance(OID, EmployeeCode)
    return {"status": "success", "data": BalanceData}



def get_leave_balanceLeaveType(OID: int, EmpCode: str,LeaveTypeID: str):
    query = Emp_Leave_Balance_Master.objects.filter(
        Emp_code=EmpCode, OrganizationID=OID, IsDelete=False,
        Leave_Type_Master=LeaveTypeID
    )

    if not (query.exists)():
        raise HTTPException(status_code=404, detail="No leave balance found")

    return (list)(query.values("Balance"))  # Convert QuerySet to List



# ✅ FastAPI route
@app.get("/LeaveBalanceByLeaveType")
def LeaveBalanceDetails(OID: int, UserID: str,LTID: str):
    EmployeeCode=""
    ed = EmployeeData(OrganizationID=OID, UserID=UserID)  # Fetch Employee Data
    if not ed or "EmployeeCode" not in ed[0]:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Employee code not found for the given UserID"}
        )

    EmployeeCode = ed[0]["EmployeeCode"]
    BalanceData = get_leave_balanceLeaveType(OID, EmployeeCode,LTID)
    return {"status": "success", "data": BalanceData}



def get_leave_type_list(OID: int):
    query = Leave_Type_Master.objects.filter(
         OrganizationID=3, IsDelete=False
    )

    if not (query.exists)():
        raise HTTPException(status_code=404, detail="No leave balance found")

    return (list)(query.values("id","Type","Description"))  # Convert QuerySet to List

@app.get("/LeaveTypeList")
def LeaveTypeList(OID: int):
    BalanceData = get_leave_type_list(OID)
    return {"status": "success", "data": BalanceData}







def get_Employee_leave_Status(OID: int, EmpCode: str,Status=None):
    if Status is None:
        Status=0
    query = Leave_Application.objects.filter(
        Emp_code=EmpCode, OrganizationID=OID, IsDelete=False,Status=Status
    ).select_related('Leave_Type_Master')

    if not (query.exists)():
        raise HTTPException(status_code=404, detail="No leave application found")

    data = (list)(query.values(
         "id", 
        "Emp_code", 
        "Start_Date", 
        "End_Date", 
        "Reason", 
        "Status", 
        "Total_credit", 
        "Remark", 
        "ReportingtoDesigantion", 
        "OrganizationID", 
        "Leave_Type_Master__id",   # Leave Type ID
        "Leave_Type_Master__Type"  # Leave Type Name
    ))
   
    for item in data:
        item["can_edit"] = item["Status"] == 0  # True if Status is 0 (Pending)
        item["can_cancel"] = item["Status"] == 0  # True if Status is 0 (Pending)
        item["Status"] = status_mapping.get(int(item["Status"]), "Unknown")

    return data
    # ✅ Rename the key
    # formatted_data = [
    #     {"Balance": item["Balance"], "Type": item["Leave_Type_Master__Type"],"ID": item["Leave_Type_Master__id"]}
    #     for item in data
    # ]

    # return formatted_data
    #return (list)(query.values("Balance","Leave_Type_Master__Type"))  # Convert QuerySet to List



# ✅ FastAPI route
@app.get("/EmployeeLeaveStatus")
def EmployeeLeaveStatus(OID: int, UserID: str, Status: int = Query(0)):
    EmployeeCode=""
    ed = EmployeeData(OrganizationID=OID, UserID=UserID)  # Fetch Employee Data
    if not ed or "EmployeeCode" not in ed[0]:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Employee code not found for the given UserID"}
        )

    EmployeeCode = ed[0]["EmployeeCode"]
    BalanceData = get_Employee_leave_Status(OID, EmployeeCode,Status)
    return {"status": "success", "data": BalanceData}






def get_Employee_leave_ApprovalList(OID: int, EmpCode: str):
    query = Leave_Application.objects.filter(
        Emp_code=EmpCode, OrganizationID=OID, IsDelete=False
    ).select_related('Leave_Type_Master')

    if not (query.exists)():
        raise HTTPException(status_code=404, detail="No leave application found")

    data = (list)(query.values())
    return data
    # ✅ Rename the key
    # formatted_data = [
    #     {"Balance": item["Balance"], "Type": item["Leave_Type_Master__Type"],"ID": item["Leave_Type_Master__id"]}
    #     for item in data
    # ]

    # return formatted_data
    #return (list)(query.values("Balance","Leave_Type_Master__Type"))  # Convert QuerySet to List



# # ✅ FastAPI route
# @app.get("/EmployeeLeaveApproval")
# def EmployeeLeaveStatus(OID: int, EmpCode: str):
#     BalanceData = get_Employee_leave_ApprovalList(OID, EmpCode)
#     return {"status": "success", "data": BalanceData}


@app.get("/approval-list/")
@app.get("/approval-list/")
def approval_list(
    OID: int,
    UserID: str,
    Status: int = Query(0),
    Start_Date: str = Query(None),
    To_Date: str = Query(None)
):
    try:
        emp_data = EmployeeData(OrganizationID=OID, UserID=UserID)
        if not emp_data or "EmployeeCode" not in emp_data[0] or "UserType" not in emp_data[0]:
            return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid employee data"})

        EmployeeCode = emp_data[0]["EmployeeCode"]
        UserType = emp_data[0]["UserType"]
        UserDepartment = emp_data[0]["Department"]

        today = datetime.now()
        # if not Start_Date:
        #     Start_Date = (today - timedelta(days=2130)).strftime('%Y-%m-%d')
        # if not To_Date:
        #     To_Date = (today + timedelta(days=300)).strftime('%Y-%m-%d')

        approval_list = []
        repdes=None
        repOid =OID
        if UserType == "CEO":
            repdes="CEO"
            approval_list = list(Leave_Application.objects.filter(
                IsDelete=False, 
                Status=Status, 
                ReportingtoDesigantion=UserType
            ).values(
                "id", 
                "Emp_code", 
                "Start_Date", 
                "End_Date", 
                "Reason", 
                "From_1st_Half",
                "From_2nd_Half",
                "To_1st_Half",
                "To_2nd_Half",
                "Status", 
                "Total_credit", 
                "Remark", 
                "ReportingtoDesigantion", 
                "OrganizationID", 
                "Leave_Type_Master__id",   # Leave Type ID
                "Leave_Type_Master__Type"  # Leave Type Name))
            ))
            repOid=None
        
        else:
            emp_details = EmployeeDataSelect(OID, EmployeeCode)
            if not emp_details:
                return JSONResponse(status_code=404, content={"status": "error", "message": "Employee designation not found"})

            Designation = emp_details[0]["Designation"]

            if emp_details[0]["Department"] == "Human Resources":
                approval_list = list(Leave_Application.objects.filter(
                    OrganizationID=OID,
                    IsDelete=False,
                    Status=Status,
                    # Start_Date__range=(Start_Date, To_Date)
                ).exclude(ReportingtoDesigantion="CEO").values(
               "id", 
                "Emp_code", 
                "Start_Date", 
                "End_Date", 
                "Reason", 
                "From_1st_Half",
                "From_2nd_Half",
                "To_1st_Half",
                "To_2nd_Half",
                "Status", 
                "Total_credit", 
                "Remark", 
                "ReportingtoDesigantion", 
                "OrganizationID", 
                "Leave_Type_Master__id",   # Leave Type ID
                "Leave_Type_Master__Type"  # Leave Type Name))
                ))
            else:
                
                approval_list = list(Leave_Application.objects.filter(
                    OrganizationID=OID,
                    IsDelete=False,
                    Status=Status,
                    # Start_Date__range=(Start_Date, To_Date),
                    ReportingtoDesigantion=Designation
                ).values(
               "id", 
                "Emp_code", 
                "Start_Date", 
                "End_Date", 
                "Reason", 
                "From_1st_Half",
                "From_2nd_Half",
                "To_1st_Half",
                "To_2nd_Half",
                "Status", 
                "Total_credit", 
                "Remark", 
                "ReportingtoDesigantion", 
                "OrganizationID", 
                "Leave_Type_Master__id",   # Leave Type ID
                "Leave_Type_Master__Type"  # Leave Type Name))
                )
                
        )
        
        if Start_Date and To_Date:
                    approval_list = approval_list.filter(Start_Date__range=(Start_Date, To_Date))

        # Convert `datetime.date` objects to string
        for application in approval_list:
            if "Start_Date" in application and isinstance(application["Start_Date"], datetime):
                application["Start_Date"] = application["Start_Date"].strftime("%Y-%m-%d")
            if "End_Date" in application and isinstance(application["End_Date"], datetime):
                application["End_Date"] = application["End_Date"].strftime("%Y-%m-%d")
        
        
        employee_mapping = {emp["EmployeeCode"]: emp for emp in EmployeeDataSelect(OrganizationID=repOid,ReportingtoDesignation=repdes)}

        employee_data = []
        for application in approval_list:
            emp_details = employee_mapping.get(application["Emp_code"])
            if emp_details:
                employee_data.append({
                    "EmpName": emp_details["EmpName"],
                    "EmployeeCode": emp_details["EmployeeCode"],
                    "LeaveApplicationDetails": application
                })
        org_ids = set(app["OrganizationID"] for app in approval_list)

        # Fetch all organization names in a single query
        org_data = OrganizationMaster.objects.filter(OrganizationID__in=org_ids, IsDelete=False).values("OrganizationID", "OrganizationName")
        org_mapping = {org["OrganizationID"]: org["OrganizationName"] for org in org_data}

        # Attach organization names to leave applications
        for application in approval_list:
            application["OrganizationName"] = org_mapping.get(application["OrganizationID"], "Unknown")
            application["can_approve"] = application["Status"] == 0  # True if Status is 0 (Pending)
            application["can_reject"] = application["Status"] == 0  # True if Status is 0 (Pending)
            application["can_revoke"] = application["Status"] == 1 and UserDepartment == 'Human Resources'  # True if Status is 0 (Pending)
            application["Status"] = status_mapping.get(int(application["Status"]), "Unknown")

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({  # Converts all non-serializable objects
                "status": "success",
                "employee_data": employee_data,
                "Status": Status,
                "Start_Date": Start_Date,
                "To_Date": To_Date
            })
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"An unexpected error occurred: "})

# ✅ Function to calculate leave credit days
def calculate_credit_days(from_date: str, to_date: str, from_half: int, to_half: int):
    # Convert dates from string to datetime
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")

    # Calculate day difference
    day_diff = (to_date - from_date).days

    if day_diff == 0:  # If it's the same day
        credit_day = 1 if (from_half == 0 and to_half == 1) else 0.5
    else:
        day_diff += 1  # Include the last day
        if from_half == 1:
            day_diff -= 0.5
        if to_half == 0:
            day_diff -= 0.5
        credit_day = day_diff

    return credit_day

# ✅ API Endpoint
@app.get("/calculate_leave_credit")
def calculate_leave_credit(
    from_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    to_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    from_half: int = Query(0, description="Is half-day on start date? 1=Yes, 0=No"),
    to_half: int = Query(1, description="Is half-day on end date? 1=Yes, 0=No")
):
    credit_days = calculate_credit_days(from_date, to_date, from_half, to_half)
    return {"LeaveCredit": credit_days}
# Define Pydantic model for request validation
class LeaveApplicationRequest(BaseModel):
    leave_id: str
    leave_type: int
    FromDate: str
    ToDate: str
    Reason: str
    LeaveCredit: decimal.Decimal
    FromHalf: int
    ToHalf: int

def EmployeeDataSelect(OrganizationID=None, EmployeeCode=None, Designation=None, ReportingtoDesignation=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "EXEC SP_EmployeeMaster_For_Leave @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s",
                [OrganizationID, EmployeeCode, Designation, ReportingtoDesignation]
            )
            rows = cursor.fetchall()
            if not rows:
                return JSONResponse(status_code=404, content={"error": "No employee data found"})

            columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Database error: {str(e)}"})




def EmployeeData(OrganizationID=None, UserID=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "EXEC SP_EmployeeMaster_Form_UserID @OrganizationID=%s, @UserID=%s",
                [OrganizationID, UserID]
            )
            rows = cursor.fetchall()
            if not rows:
                return JSONResponse(status_code=404, content={"error": "No employee data found"})

            columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Database error: {str(e)}"})

def CombinedLeaveInfo(UserID, OrganizationID, LeaveID, EmployeeCode, SelectedLeaveType, LeaveCredit, Start_Date, End_Date):
    error_messages = []

    try:
        current_year = datetime.now().year

        objconfig = get_object_or_404(
            Leave_Config_Details,
            Leave_Type_Master_id=LeaveID,
            IsDelete=False,
            Financial_Year_Start_Date__year=current_year
        )

        LeaveCountObj = Leave_Application.objects.filter(
            Leave_Type_Master_id=LeaveID,
            Emp_code=EmployeeCode,
            Start_Date__year=current_year,
            IsDelete=False,
            Status=1,
            OrganizationID=OrganizationID,
        )

        Apply_Max = objconfig.Apply_Max
        Apply_Min = objconfig.Apply_Min
        IsConfirmed = objconfig.IsConfirmed

        if IsConfirmed:
            EmpStatusObj = EmployeeDataSelect(OrganizationID, EmployeeCode)
            EmpStatus = EmpStatusObj[0]['EmpStatus'] if EmpStatusObj else None

            if EmpStatus != 'Confirmed':
                error_messages.append(f"Cannot apply for {SelectedLeaveType}, employee status is {EmpStatus}")

        LeaveCount = LeaveCountObj.count() or 0

        if LeaveCount >= objconfig.Appn_Times:
            error_messages.append(f"You cannot apply for {SelectedLeaveType} more than {objconfig.Appn_Times} times in a year")

        if LeaveCredit < Apply_Min:
            error_messages.append(f"You cannot apply for {SelectedLeaveType} with less than {Apply_Min} leave balance")

        if LeaveCredit > Apply_Max:
            error_messages.append(f"You cannot apply for {SelectedLeaveType} with more than {Apply_Max} leave balance")

        CheckBalance = Emp_Leave_Balance_Master.objects.filter(
            Leave_Type_Master_id=LeaveID,
            Emp_code=EmployeeCode,
            IsDelete=False,
            OrganizationID=OrganizationID
        ).first()

        if CheckBalance:
            RemainingBalance = CheckBalance.Balance - LeaveCredit
            if RemainingBalance < decimal.Decimal('0.00'):
                error_messages.append(f"Your {CheckBalance.Leave_Type_Master.Type} balance is {CheckBalance.Balance}. You are applying for {LeaveCredit}")

        IsDate = objconfig.IsDate

        if IsDate and Start_Date:
            optional_holidays = Optional_Holidays.objects.filter(
                Date=Start_Date,
                Is_Active=True,
                IsDelete=False
            )
            if not optional_holidays.exists():
                formatted_date = datetime.strptime(Start_Date, "%Y-%m-%d").strftime("%d-%m-%y")
                error_messages.append(f"No {SelectedLeaveType} is present for {formatted_date}")

        if error_messages:
            return JSONResponse(status_code=400, content={"status": "error", "messages": error_messages})

        return JSONResponse(status_code=200, content={"status": "success"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "messages": [f"An unexpected error occurred: {str(e)}"]})

def create_or_update_leave_application(OrganizationID: int, UserID: str, EmployeeCode: str, request_data: LeaveApplicationRequest):
    try:
        ReportingtoDesigantion =""
        ed = EmployeeData(OrganizationID=OrganizationID,UserID=UserID)
        if ed is not None: 
            ReportingtoDesigantion = ed[0]["ReportingtoDesigantion"]
            EmployeeCode=ed[0]["EmployeeCode"]
        if request_data.leave_id:
            leave = Leave_Application.objects.filter(
                id=request_data.leave_id, OrganizationID=OrganizationID, IsDelete=False
            ).first()
            if not leave:
                return JSONResponse(status_code=404, content={"error": "No leave type found"})

            leave_type = Leave_Type_Master.objects.get(id=request_data.leave_type, IsDelete=False, Is_Active=True)
            Start_Date = request_data.FromDate
            End_Date = request_data.ToDate
            LeaveCredit = request_data.LeaveCredit

            Info = CombinedLeaveInfo(UserID, OrganizationID, leave_type.id, EmployeeCode, leave_type.Type, LeaveCredit, Start_Date, End_Date)
            if Info.status_code != 200:
                return Info

            leave.Leave_Type_Master = leave_type
            leave.Start_Date = Start_Date
            leave.End_Date = End_Date
            leave.Reason =request_data.Reason
            leave.Total_credit = LeaveCredit
            leave.ModifyBy = UserID
            leave.save()

            return JSONResponse(status_code=200, content={"status": "success", "message": "Leave updated successfully"})

        else:
            leave_type = Leave_Type_Master.objects.get(id=request_data.leave_type, IsDelete=False, Is_Active=True)
            Start_Date = request_data.FromDate
            End_Date = request_data.ToDate
            LeaveCredit = request_data.LeaveCredit

            Info = CombinedLeaveInfo(UserID, OrganizationID, leave_type.id, EmployeeCode, leave_type.Type, LeaveCredit, Start_Date, End_Date)
            if Info.status_code != 200:
                return Info

            Leave_Application.objects.create(
                OrganizationID=OrganizationID,
                Status=0,
                CreatedBy=UserID,
                Leave_Type_Master=leave_type,
                Start_Date=Start_Date,
                End_Date=End_Date,
                Reason=request_data.Reason,
                Total_credit=LeaveCredit,
                Emp_code=EmployeeCode,
                ReportingtoDesigantion=ReportingtoDesigantion
            )

            return JSONResponse(status_code=201, content={"status": "success", "message": "Leave applied successfully"})

    except Leave_Type_Master.DoesNotExist:
        return JSONResponse(status_code=404, content={"error": "Invalid leave type"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})

@app.post("/leave-application/")
def leave_application(
    OID: int = Form(...),
    EmpCode: str = Form(...),
    UserID: str = Form(...),
    leave_type: int = Form(...),
    FromDate: str = Form(...),
    ToDate: str = Form(...),
    Reason: str = Form(...),
    LeaveCredit: decimal.Decimal = Form(...),
    FromHalf: int = Form(...),
    ToHalf: int = Form(...),
    leave_id: str = Form(None),
):
    request = LeaveApplicationRequest(
        leave_id=leave_id or "",
        leave_type=leave_type,
        FromDate=FromDate,
        ToDate=ToDate,
        Reason=Reason,
        LeaveCredit=LeaveCredit,
        FromHalf=FromHalf,
        ToHalf=ToHalf
    )
    result = create_or_update_leave_application(OID, UserID, EmpCode, request)
    return result# @app.get("/OpenPositionList", response_model=List[dict])



    # ReportingtoDesigantion: str = Field(..., title="Reporting to Designation", description="Reporting designation")

from app.send_notification import *

@app.post("/approve-leave/")
def approve_leave(leave_id: int=Form(...),    OID: int=Form(...),    UserID:int=Form(...)):
    try:
        user_id = UserID  # Get authenticated user ID
        application_id = leave_id
        organization_id = OID

        # Fetch leave application
        leave_application = Leave_Application.objects.filter(
            id=application_id, IsDelete=False
        ).first()

        if not leave_application:
            raise HTTPException(status_code=404, detail="Leave application not found")

        OgID = leave_application.OrganizationID
        emp_code = leave_application.Emp_code
        leave_start_date = leave_application.Start_Date
        leave_end_date = leave_application.End_Date

        
        current_date = leave_start_date
       
            
        while current_date <= leave_end_date:
            duplicates = Attendance_Data.objects.filter(
                        Date=current_date,
                        IsDelete=False,
                        EmployeeCode=emp_code,
                        OrganizationID=OgID
                    )

            if duplicates.count() > 1:
                # Decide which one to keep and delete the rest
                duplicates.exclude(id=duplicates.first().id).delete()
            attendance_record, created = Attendance_Data.objects.update_or_create(
                Date=current_date,
                IsDelete=False,
                EmployeeCode=emp_code,
                OrganizationID=OgID,
                defaults={
                    "IsDelete": False,
                    "Status": leave_application.Leave_Type_Master.Type,
                    "ModifyBy": user_id,
                }
            )
            current_date += timedelta(days=1)

        # Update leave application status
        leave_application.Status = 1  # Approved
        leave_application.ModifyBy = user_id
        leave_application.save()


        hops_id = str(application_id)

        Send_Leave_Approval_Notification(
            organization_id=OgID,
            EmpCode=emp_code,
            title=f"Leave is approved",
            message=f"New Leave Approved",
            module_name="LeaveManagementSystem",
            action="Approved",
            hopsId=hops_id,
            user_type="admin",
            priority="high"
        )

        return JSONResponse(status_code=200, content={"status": "success", "message": "Leave Approved Successfully"})

        

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"An error occurred: {str(e)}"})


@app.post("/reject-leave/")
def reject_leave(
    leave_id: int = Form(...),
    OID: int = Form(...),
    UserID: int = Form(...),
    Remark: str = Form(...)
):
    try:
        user_id = UserID  # Authenticated user ID
        application_id = leave_id
        organization_id = OID

        
        # Fetch the leave application
        leave_application = get_object_or_404(
            Leave_Application, id=application_id, OrganizationID=organization_id, IsDelete=False
        )
        if leave_application is not None:
            emp_code = leave_application.Emp_code or 0
            OgID = leave_application.OrganizationID

            # Update leave status to rejected
            leave_application.Status = -1  # Rejected
            leave_application.ModifyBy = user_id
            leave_application.Remark = Remark
            leave_application.save()

            hops_id = str(application_id)

            Send_Leave_Approval_Notification(
                organization_id=OgID,
                EmpCode=emp_code,
                title=f"Leave is Rejected",
                message=f"Leave Is Rejected",
                module_name="LeaveManagementSystem",
                action="Rejected",
                hopsId=hops_id,
                user_type="admin",
                priority="high"
            )


            # Restore Leave Balance
            leave_balance = Emp_Leave_Balance_Master.objects.filter(
                Leave_Type_Master=leave_application.Leave_Type_Master,
                Emp_code=leave_application.Emp_code,
                OrganizationID=organization_id,
                IsDelete=False
            ).first()

            # Get last leave debit record
            leave_debit = EmpMonthLevelDebitMaster.objects.filter(
                Leave_Type_Master=leave_application.Leave_Type_Master,
                OrganizationID=organization_id,
                Emp_code=leave_application.Emp_code,
                debit=leave_application.Total_credit
            ).order_by('-CreatedDateTime').first()

            if leave_balance and leave_debit:
                leave_balance.Balance += leave_debit.debit
                leave_balance.save()

            return JSONResponse(status_code=200, content={"status": "success", "message": "Leave Rejected Successfully"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"An error occurred: {str(e)}"})

@app.post("/revoke-leave/")
def revoke_leave(
    leave_id: int = Form(...),
    OID: int = Form(...),
    UserID: int = Form(...)
):
    try:
        application_id = leave_id
        organization_id = OID
        user_id = UserID  # Authenticated user ID

    
        # Fetch the leave application
        leave_application = get_object_or_404(
            Leave_Application, id=application_id, OrganizationID=organization_id, IsDelete=False
        )

        leave_type = leave_application.Leave_Type_Master
        debit = leave_application.Total_credit
        emp_code = leave_application.Emp_code

        # Restore Leave Balance
        leave_balance = Emp_Leave_Balance_Master.objects.filter(
            Leave_Type_Master=leave_type,
            Emp_code=emp_code,
            OrganizationID=organization_id,
            IsDelete=False
        ).first()

        # Get last leave debit record
        leave_debit = EmpMonthLevelDebitMaster.objects.filter(
            Leave_Type_Master=leave_type,
            OrganizationID=organization_id,
            Emp_code=emp_code,
            debit=debit
        ).order_by('-CreatedDateTime').first()

        if leave_balance and leave_debit:
            leave_balance.Balance += leave_debit.debit
            leave_balance.save()

        # Update Attendance Records
        leave_start_date = leave_application.Start_Date
        leave_end_date = leave_application.End_Date

        try:
            attendance_records = Attendance_Data.objects.filter(
                Date__range=(leave_start_date, leave_end_date),
                OrganizationID=organization_id,
                IsDelete=False,
                EmployeeCode=emp_code
            )

            for attendance in attendance_records:
                if attendance.In_Time and attendance.Out_Time:
                    status = "Present"
                elif attendance.In_Time or attendance.Out_Time:
                    status = "Absent"
                else:
                    status = "Unknown"

                attendance.Status = status
                attendance.ModifyBy = user_id
                attendance.save()
        except Exception as e:
            print(f"Error updating attendance: {e}")

        # Mark Leave as Revoked
        leave_application.Status = 2  # Revoked
        leave_application.ModifyBy = user_id
        leave_application.save()

        return JSONResponse(status_code=200, content={"status": "success", "message": "Leave Revoked Successfully"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"An error occurred: {str(e)}"})
    

@app.post("/comp-off-application/")
def create_comp_off_application(
    OID: int = Form(...),
    UserID: int = Form(...),
    CompOff_Date: str = Form(...),
    Reason: str = Form(...)
):
    try:
        # Fetch Employee Code
        EmployeeCode = ""
        ReportingtoDesigantion = ""

        ed = EmployeeData(OrganizationID=OID, UserID=UserID)
        if ed is not None: 
            EmployeeCode = ed[0]["EmployeeCode"]
            ReportingtoDesigantion = ed[0]["ReportingtoDesigantion"]

        if not EmployeeCode:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Employee code not found for the given UserID"}
            )

        # Create the CompOff application
        application = CompOffApplication.objects.create(
            OrganizationID=OID,
            Status="Pending",
            CreatedBy=UserID,
            CompOff_Date=CompOff_Date,
            Reason=Reason,
            Emp_Code=EmployeeCode,
            ReportingtoDesigantion=ReportingtoDesigantion,
        )

        return JSONResponse(
            status_code=201,
            content={
                "status": "success",
                "message": "Comp-off application created successfully",
                "application_id": application.id
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
        )

@app.get("/comp-off-claim-status/")
def comp_off_claim_status(OID: int, UserID: str):
    try:
        # Fetch Employee Data
        ed = EmployeeData(OrganizationID=OID, UserID=UserID)  # Fetch Employee Data
        if not ed or "EmployeeCode" not in ed[0]:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Employee code not found for the given UserID"}
            )

        EmployeeCode = ed[0]["EmployeeCode"]

        # Fetch comp-off status using Django ORM
        status_entries = CompOffApplication.objects.filter(
            OrganizationID=OID,
            Emp_Code=EmployeeCode,
            IsDelete=False
        )

        if not status_entries.exists():
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": "No comp-off applications found"}
            )

        # Format response data
        status_list = [
            {
                "application_id": entry.id,
                "comp_off_date": entry.CompOff_Date.strftime("%Y-%m-%d"),
                "reason": entry.Reason,
                "status": entry.Status
            }
            for entry in status_entries
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "current_date": str(date.today()),
                "applications": status_list
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
        )




@app.get("/comp-off-approval-list/")
def comp_off_approval_list(
    OID: int,
    UserID: str,
    
  
    Status: str = Query(default="Pending"),
    Start_Date: str = None,
    To_Date: str = None
):
    try:
        # Default date range: Last 30 days to Next 30 days
        EmployeeCode=""
        ed = EmployeeData(OrganizationID=OID, UserID=UserID)  # Fetch Employee Data
        if not ed or "EmployeeCode" not in ed[0]:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Employee code not found for the given UserID"}
            )

        EmployeeCode = ed[0]["EmployeeCode"]
        UserType= ed[0]["UserType"]
        today = datetime.now()
        # Start_Date = Start_Date or (today - timedelta(days=2130)).strftime('%Y-%m-%d')
        # To_Date = To_Date or (today + timedelta(days=2130)).strftime('%Y-%m-%d')

        approval_list = []

        # If user is CEO, fetch all comp-off requests under their approval
        if UserType == "CEO":
            approval_list = CompOffApplication.objects.filter(
                OrganizationID=OID,
                IsDelete=False,
                Status=Status,
                ReportingtoDesigantion="CEO"
            )

            # Fetch employees reporting to CEO
            Empobjs = EmployeeDataSelect(ReportingtoDesignation="CEO")
            employee_mapping = {emp['EmployeeCode']: emp for emp in Empobjs}

        else:
            if EmployeeCode:
                # Fetch employee designation
                emp_data = EmployeeDataSelect(OID, EmployeeCode)
                if not emp_data:
                    return JSONResponse(
                        status_code=400,
                        content={"status": "error", "message": "Employee details not found. Contact HR."}
                    )

                Designation = emp_data[0]['Designation']
                Department = emp_data[0]['Department']

                # HR can view all applications except CEO's
                if Department == 'Human Resources':
                    approval_list = list(CompOffApplication.objects.filter(
                        OrganizationID=OID,
                        IsDelete=False,
                        Status=Status,
                        CompOff_Date__range=(Start_Date, To_Date)
                    ).exclude(ReportingtoDesigantion="CEO").values())
                else:
                    approval_list = list(CompOffApplication.objects.filter(
                        OrganizationID=OID,
                        IsDelete=False,
                        Status=Status,
                        CompOff_Date__range=(Start_Date, To_Date),
                        ReportingtoDesigantion=Designation
                    ).values())

                # Fetch all employees in the organization
                Empobjs = EmployeeDataSelect(OID)
                employee_mapping = {emp['EmployeeCode']: emp for emp in Empobjs}
            else:
                return JSONResponse(
                    status_code=400,
                    content={"status": "error", "message": "Employee code not found. Contact HR."}
                )
        org_ids = set(app["OrganizationID"] for app in approval_list)

        # Fetch all organization names in a single query
        org_data = OrganizationMaster.objects.filter(OrganizationID__in=org_ids, IsDelete=False).values("OrganizationID", "OrganizationName")
        org_mapping = {org["OrganizationID"]: org["OrganizationName"] for org in org_data}

        # Attach organization names to leave applications
        for application in approval_list:
            application["OrganizationName"] = org_mapping.get(application["OrganizationID"], "Unknown")
        # Format response data
        employee_data = []
        for application in approval_list:
            emp_details = employee_mapping.get(application["Emp_Code"])
            if emp_details:
                employee_data.append({
                    "EmpName": emp_details['EmpName'],
                    "EmployeeCode": emp_details['EmployeeCode'],
                    "OrganizationName":application["OrganizationName"],
                    "CompOffApplicationDetails": {
                        "application_id": application["id"],
                        "comp_off_date": application["CompOff_Date"].strftime("%Y-%m-%d"),
                        "reason": application["Reason"],
                        "status": application["Status"],
                        "can_approve": application["Status"]=="Pending",
                        "can_reject": application["Status"]=="Pending"
                        
                    }
                })

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "applications": employee_data,
                "Status": Status,
                "Start_Date": Start_Date,
                "To_Date": To_Date
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
        )
    


@app.post("/approve-comp-off/")
def approve_comp_off_leave(
    application_id: int = Form(...),
    OID: int = Form(...),
    UserID: int = Form(...)
):
    try:
        application_id = application_id
        organization_id = OID
        user_id = UserID  # Authenticated user ID

    
        # Fetch the leave application
        comp_off_application = get_object_or_404(
            CompOffApplication, id=application_id, OrganizationID=organization_id, IsDelete=False
        )

        emp_code = comp_off_application.Emp_Code

        # Approve the Comp-Off leave
        comp_off_application.Status = "Approved"
        comp_off_application.ModifyBy = user_id
        comp_off_application.save()

        balance = 1  # Default balance increment for comp-off

        # Fetch "Comp-off" leave type
        leave_type_obj = Leave_Type_Master.objects.filter(
            IsDelete=False, OrganizationID=3, Type="Comp-off"
        ).first()

        if not leave_type_obj:
            raise HTTPException(status_code=404, detail="Comp-off leave type not found")

        # Update or create leave balance
        leave_balance = Emp_Leave_Balance_Master.objects.filter(
            Leave_Type_Master=leave_type_obj,
            Emp_code=emp_code,
            OrganizationID=organization_id,
            IsDelete=False
        ).first()

        if leave_balance:
            leave_balance.Balance += balance
            leave_balance.ModifyBy = user_id
            leave_balance.save()
        else:
            Emp_Leave_Balance_Master.objects.create(
                OrganizationID=organization_id,
                Leave_Type_Master=leave_type_obj,
                Emp_code=emp_code,
                Balance=balance,
                CreatedBy=user_id
            )

        # Add credit record
        EmpMonthLevelCreditMaster.objects.create(
            Leave_Type_Master=leave_type_obj,
            OrganizationID=organization_id,
            Emp_code=emp_code,
            credit=balance,
            CreatedBy=user_id
        )

        return JSONResponse(status_code=200, content={"status": "success", "message": "Comp-Off Approved Successfully"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"An error occurred: {str(e)}"})





@app.post("/reject-comp-off/")
def approve_comp_off_leave(
    application_id: int = Form(...),
    OID: int = Form(...),
    UserID: int = Form(...)
):
    try:
        application_id = application_id
        organization_id = OID
        user_id = UserID  # Authenticated user ID

    
        # Fetch the leave application
        comp_off_application = get_object_or_404(
            CompOffApplication, id=application_id, OrganizationID=organization_id, IsDelete=False
        )

        emp_code = comp_off_application.Emp_Code

        # Approve the Comp-Off leave
        comp_off_application.Status = "Rejected"
        comp_off_application.ModifyBy = user_id
        comp_off_application.save()


        return JSONResponse(status_code=200, content={"status": "success", "message": "Comp-Off Rejected Successfully"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"An error occurred: {str(e)}"})

@app.get("/DashboardCalendar/")
def DashboardCalendar(OID: int,
    UserID: str,
    UserType:str):
    
    OrganizationID = OID
    UserID = UserID
    UserType = UserType
    Department_Name=""
    
    Emp_code=""
    ed = EmployeeData(OrganizationID=OID, UserID=UserID)  # Fetch Employee Data
    if not ed or "EmployeeCode" not in ed[0]:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Employee code not found for the given UserID"}
        )

    Emp_code = ed[0]["EmployeeCode"]
    Department_Name = ed[0]["Department"]
    
    all_leaves = Leave_Application.objects.filter(IsDelete=False,OrganizationID=OrganizationID, Emp_code=Emp_code)
    
    leave_list = []

    for leave in all_leaves:
      leave_dict = {
        'title': leave.Leave_Type_Master.Type,
        'classes':'myclass',
         'id': leave.id,
         'status':leave.Status,
         'start': leave.Start_Date.strftime('%Y-%m-%d'),  
         'end': leave.End_Date.strftime('%Y-%m-%d 23:00'),      
      }
      leave_list.append(leave_dict)
   
    return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "applications": leave_list,
            }
        )

@app.get("/employee-dashboard/")
def employee_dashboard(OID: int, UserID: str):
    try:
        # Fetch Employee Code
        Emp_code = ""
        ed = EmployeeData(OrganizationID=OID, UserID=UserID)
        if not ed or "EmployeeCode" not in ed[0]:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Employee code not found for the given UserID"}
            )

        Emp_code = ed[0]["EmployeeCode"]
        UserType = ed[0]["UserType"]
        UserDepartment = ed[0]["Department"]
        print(UserDepartment)
        print(UserType)
        # Fetch Leave Balance
        leave_balance = Emp_Leave_Balance_Master.objects.select_related("Leave_Type_Master").filter(
            OrganizationID=OID, IsDelete=False, Emp_code=Emp_code
        )

        total_leave_balance = sum(float(leave.Balance) for leave in leave_balance)  # Convert Decimal to float

        # Fetch Leave Requests
        leave_request_pending = Leave_Application.objects.filter(
            OrganizationID=OID, IsDelete=False, Emp_code=Emp_code, Status=0
        ).count()

        leave_request_rejected = Leave_Application.objects.filter(
            OrganizationID=OID, IsDelete=False, Emp_code=Emp_code, Status=-1
        ).count()

        leave_request_approved = Leave_Application.objects.filter(
            OrganizationID=OID, IsDelete=False, Emp_code=Emp_code, Status=1
        ).count()

        # Format leave balance details (Convert Decimal to float)
        leave_balance_data = [
            {
                "LeaveType": leave.Leave_Type_Master.Type,  # Fetch Leave Type
                "Balance": float(leave.Balance)  # Convert Decimal to float
            }
            for leave in leave_balance
        ]

        pending_leave_approvals = 0  # Default Value
        pending_compoff_approvals=0
        if UserType == "CEO":
            
            repOid =OID
            repdes="CEO"
            approval_list =  list(Leave_Application.objects.filter(
                IsDelete=False, Status=0, ReportingtoDesigantion="CEO"
            ).values(
                "id", 
                "Emp_code", 
                "Start_Date", 
                "End_Date", 
                "Reason", 
                "From_1st_Half",
                "From_2nd_Half",
                "To_1st_Half",
                "To_2nd_Half",
                "Status", 
                "Total_credit", 
                "Remark", 
                "ReportingtoDesigantion", 
                "OrganizationID", 
                "Leave_Type_Master__id",   # Leave Type ID
                "Leave_Type_Master__Type"  # Leave Type Name))
            ))
            
            
            employee_mapping = {emp["EmployeeCode"]: emp for emp in EmployeeDataSelect(ReportingtoDesignation=repdes)}

            employee_data = []
            for application in approval_list:
                emp_details = employee_mapping.get(application["Emp_code"])
                if emp_details:
                    employee_data.append({
                        "EmpName": emp_details["EmpName"],
                        "EmployeeCode": emp_details["EmployeeCode"],
                        "LeaveApplicationDetails": application
                    })
                    
            pending_leave_approvals=employee_data.count("id")
            CompOffApplicationLst = list(CompOffApplication.objects.filter(
                IsDelete=False, Status="Pending", ReportingtoDesigantion="CEO"
            ).values())
            Compemployee_data = []
            for application in CompOffApplicationLst:
                emp_details = employee_mapping.get(application["Emp_Code"])
                if emp_details:
                    Compemployee_data.append({
                        "EmpName": emp_details["EmpName"],
                        "EmployeeCode": emp_details["EmployeeCode"],
                        "LeaveApplicationDetails": application
                    })
            pending_compoff_approvals=Compemployee_data.count("id")
        elif UserDepartment == "Human Resources":
            pending_leave_approvals = Leave_Application.objects.filter(
                OrganizationID=OID, IsDelete=False, Status=0
            ).exclude(ReportingtoDesigantion="CEO").count()

            pending_compoff_approvals = CompOffApplication.objects.filter(
                OrganizationID=OID, IsDelete=False, Status="Pending", ReportingtoDesigantion="CEO"
            ).exclude(ReportingtoDesigantion="CEO").count()
        else:
            # Fetch Employee Designation
            pending_leave_approvals = Leave_Application.objects.filter(
                OrganizationID=OID, IsDelete=False, Status=0, ReportingtoDesigantion=ed[0]["Designation"]
            ).count()
        
        
        pending_compoff_approvals = CompOffApplication.objects.filter(
            OrganizationID=OID, IsDelete=False, Status=0, ReportingtoDesigantion=ed[0]["Designation"]
        ).count()
    
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "total_leave_balance": total_leave_balance,
                "leave_request_pending_count": leave_request_pending,
                "leave_request_rejected_count": leave_request_rejected,
                "leave_request_approved_count": leave_request_approved,
                "total_pending_leave_approvel": pending_leave_approvals,
                "total_pending_compoff_approvel": pending_compoff_approvals,
                "leave_balance_details": leave_balance_data,
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
        )



@app.post("/leave-application-cancel/")
def leave_application_cancel(
    OID: str = Form(...),
    UserID: str = Form(...),
    leave_id: str = Form(...)
):
    try:
            # Fetch Leave Application
            leave_app = Leave_Application.objects.filter(id=leave_id, IsDelete=False,Status=-1).first()
            if not leave_app:
                #raise HTTPException(status_code=404, detail="Leave application not found")
                return JSONResponse(status_code=404, content={"status": "error", "message": f"Leave application not found."})

            # Mark Leave as Deleted
            #leave_app.IsDelete = True
            leave_app.Status=-1
            leave_app.ModifyBy = UserID
            leave_app.save()

            # Fetch Leave Balance
            leave_balance = Emp_Leave_Balance_Master.objects.filter(
                Leave_Type_Master=leave_app.Leave_Type_Master,
                Emp_code=leave_app.Emp_code,
                OrganizationID=OID,
                IsDelete=False
            ).first()
            try:
                if not leave_balance:
                    raise HTTPException(status_code=400, detail="Leave balance record not found")

                # Fetch Last Leave Debit Entry
                leave_debit = EmpMonthLevelDebitMaster.objects.filter(
                    Leave_Type_Master=leave_app.Leave_Type_Master,
                    OrganizationID=OID,
                    Emp_code=leave_app.Emp_code,
                    debit=leave_app.Total_credit
                ).order_by('-CreatedDateTime').first()

                if not leave_debit:
                    raise HTTPException(status_code=400, detail="Leave debit record not found")

                # Restore Balance
                leave_balance.Balance += leave_debit.debit
                leave_balance.save()
            except:
                print()
            return JSONResponse(
                status_code=200,
                content={"status": "success", "message": "Leave application canceled successfully"}
            )

    except HTTPException as http_err:
        #return JSONResponse(status_code=http_err.status_code, content={"status": "error", "message": http_err.detail})
        return JSONResponse(status_code=http_err.status_code, content={"status": "error", "message": f"An unexpected error occurred."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"An unexpected error occurred."})
# def get_open_positions():
    
#     positions = OpenPosition.objects.filter(IsDelete=False, Status=1).order_by('-CreatedDateTime')  
    
#     positions_list = []
#     for position in positions.values():
        
        
#         for key, value in position.items():
#             if isinstance(value, datetime):  
#                 position[key] = value.isoformat()  
#             elif isinstance(value, date):  
#                 position[key] = value.isoformat()  
#         positions_list.append(position)
    
#     return JSONResponse(content=positions_list)



# @app.get("/get_open_positionLocationWise", response_model=List[dict])
# def get_open_positionLocationWise(Location):
#     positions = OpenPosition.objects.filter(IsDelete=False,Status=1)
#     positions_list = []
#     for position in positions.values():
        
#         for key, value in position.items():
#             if isinstance(value, datetime):  
#                 position[key] = value.isoformat()  
#             elif isinstance(value, date):  
#                 position[key] = value.isoformat()  
#         positions_list.append(position)
    
#     return JSONResponse(content=positions_list)
    
# @app.get("/get_open_positionname", response_model=List[str])  # List of strings (Position names)
# def get_open_positionname(Location):
#     positions = OpenPosition.objects.filter(IsDelete=False, Status=1)
    
#     # Extract the 'Position' values directly
#     positions_values = [position['Position'] for position in positions.values('Position')]

#     return JSONResponse(content=positions_values)
