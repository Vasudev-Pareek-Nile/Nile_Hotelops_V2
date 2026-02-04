from http.client import HTTPException
import json
import os
import traceback
import django
from html5lib import serialize
from requests import Request, Session
from fastapi import FastAPI, Depends, Query
from django.db import models
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
import sys
import django



VALID_TOKENS = {"ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f"}
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelopsmgmtpy.settings')
django.setup()

from django.db import connection


from Leave_Management_System.models import Emp_Leave_Balance_Master, Leave_Application, Leave_Type_Master
from Open_position.models import OpenPosition

from datetime import date

app = FastAPI()

@app.middleware("http")
async def check_hotel_api_token(request: Request, call_next):
    token = request.headers.get("hotel-api-token")
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:  
        response = await call_next(request)
        return response
    if not token:
        return HTTPException(status_code=400, detail="Missing 'hotel-api-token' header")

    if token not in VALID_TOKENS:
        return HTTPException(status_code=403, detail="Invalid 'hotel-api-token' value")

    response = await call_next(request)
    return response

@app.get("/")
async def read_root():
    return {"message": "Token is valid"}

@app.get("/another-endpoint")
async def another_route():
    return {"message": "Another endpoint accessed with valid token"}

from asgiref.sync import sync_to_async
async def get_leave_balance(OID: int, EmpCode: str):
    query = Emp_Leave_Balance_Master.objects.filter(
        Emp_code=EmpCode, OrganizationID=OID, IsDelete=False
    ).select_related('Leave_Type_Master')

    if not await sync_to_async(query.exists)():
        raise HTTPException(status_code=404, detail="No leave balance found")

    data = await sync_to_async(list)(query.values("Balance", "Leave_Type_Master__Type", "Leave_Type_Master__id"))

    # ✅ Rename the key
    formatted_data = [
        {"Balance": item["Balance"], "Type": item["Leave_Type_Master__Type"],"ID": item["Leave_Type_Master__id"]}
        for item in data
    ]

    return formatted_data
    #return await sync_to_async(list)(query.values("Balance","Leave_Type_Master__Type"))  # Convert QuerySet to List



# ✅ FastAPI async route
@app.get("/LeaveBalance")
async def LeaveBalanceDetails(OID: int, EmpCode: str):
    BalanceData = await get_leave_balance(OID, EmpCode)
    return {"status": "success", "data": BalanceData}



async def get_leave_balanceLeaveType(OID: int, EmpCode: str,LeaveTypeID: str):
    query = Emp_Leave_Balance_Master.objects.filter(
        Emp_code=EmpCode, OrganizationID=OID, IsDelete=False,
        Leave_Type_Master=LeaveTypeID
    )

    if not await sync_to_async(query.exists)():
        raise HTTPException(status_code=404, detail="No leave balance found")

    return await sync_to_async(list)(query.values("Balance"))  # Convert QuerySet to List



# ✅ FastAPI async route
@app.get("/LeaveBalanceByLeaveType")
async def LeaveBalanceDetails(OID: int, EmpCode: str,LTID: str):
    BalanceData = await get_leave_balanceLeaveType(OID, EmpCode,LTID)
    return {"status": "success", "data": BalanceData}



async def get_leave_type_list(OID: int):
    query = Leave_Type_Master.objects.filter(
         OrganizationID=3, IsDelete=False
    )

    if not await sync_to_async(query.exists)():
        raise HTTPException(status_code=404, detail="No leave balance found")

    return await sync_to_async(list)(query.values("id","Type","Description"))  # Convert QuerySet to List

@app.get("/LeaveTypeList")
async def LeaveTypeList(OID: int):
    BalanceData = await get_leave_type_list(OID)
    return {"status": "success", "data": BalanceData}







async def get_Employee_leave_Status(OID: int, EmpCode: str):
    query = Leave_Application.objects.filter(
        Emp_code=EmpCode, OrganizationID=OID, IsDelete=False
    ).select_related('Leave_Type_Master')

    if not await sync_to_async(query.exists)():
        raise HTTPException(status_code=404, detail="No leave application found")

    data = await sync_to_async(list)(query.values())
    return data
    # ✅ Rename the key
    # formatted_data = [
    #     {"Balance": item["Balance"], "Type": item["Leave_Type_Master__Type"],"ID": item["Leave_Type_Master__id"]}
    #     for item in data
    # ]

    # return formatted_data
    #return await sync_to_async(list)(query.values("Balance","Leave_Type_Master__Type"))  # Convert QuerySet to List



# ✅ FastAPI async route
@app.get("/EmployeeLeaveStatus")
async def EmployeeLeaveStatus(OID: int, EmpCode: str):
    BalanceData = await get_Employee_leave_Status(OID, EmpCode)
    return {"status": "success", "data": BalanceData}






async def get_Employee_leave_ApprovalList(OID: int, EmpCode: str):
    query = Leave_Application.objects.filter(
        Emp_code=EmpCode, OrganizationID=OID, IsDelete=False
    ).select_related('Leave_Type_Master')

    if not await sync_to_async(query.exists)():
        raise HTTPException(status_code=404, detail="No leave application found")

    data = await sync_to_async(list)(query.values())
    return data
    # ✅ Rename the key
    # formatted_data = [
    #     {"Balance": item["Balance"], "Type": item["Leave_Type_Master__Type"],"ID": item["Leave_Type_Master__id"]}
    #     for item in data
    # ]

    # return formatted_data
    #return await sync_to_async(list)(query.values("Balance","Leave_Type_Master__Type"))  # Convert QuerySet to List



# ✅ FastAPI async route
@app.get("/EmployeeLeaveApproval")
async def EmployeeLeaveStatus(OID: int, EmpCode: str):
    BalanceData = await get_Employee_leave_ApprovalList(OID, EmpCode)
    return {"status": "success", "data": BalanceData}



# @app.get("/OpenPositionList", response_model=List[dict])
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
