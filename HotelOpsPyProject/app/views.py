from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from requests import Session, post
import requests
from . import forms, models
from django.contrib.auth.models import Group
from .models import *
from django.shortcuts import render, redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from rest_framework import viewsets

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import UserSession
from .serializers import UserSessionSerializer

class UserSessionViewSet(viewsets.ViewSet):
    def retrieve(self, request, user_id=None):
        user_id=decrypt_id(user_id)
        # Check if the user_id is provided and is a valid integer
        if not user_id :
            return Response({"error": "Invalid user_id"}, status=400)
        
        try:
            # Fetch the UserSession object for the given user_id
          
            print(user_id)
            user_session = UserSession.objects.get(user_id=user_id)
            
            # Serialize the user session data
            serializer = UserSessionSerializer(user_session)
            
            # Return the serialized data as a response
            return Response(serializer.data)
        
        except UserSession.DoesNotExist:
            # Handle case where the UserSession does not exist
            return Response({"error": "User session not found"}, status=404)
        
        except Exception as e:
            # Handle any other unexpected errors
            return Response({"error": str(e)}, status=500)


def netlogredre(request):
  
    AuthToken = request.GET.get('AuthToken', "")
    print(AuthToken)
    AuthToken="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMDIyMTEwNTE2ODMwOCIsImlzcyI6ImZpcmViYXNlLWFkbWluc2RrLW9wbjd2QGhvdGVsb3BzLThkZjk5LmlhbS5nc2VydmljZWFjY291bnQuY29tIiwic3ViIjoiZmlyZWJhc2UtYWRtaW5zZGstb3BuN3ZAaG90ZWxvcHMtOGRmOTkuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJhdWQiOiJodHRwczovL2lkZW50aXR5dG9vbGtpdC5nb29nbGVhcGlzLmNvbS9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsImV4cCI6MTczNzYyMzAxNCwiaWF0IjoxNzM3NjE5NDE0fQ.Es0mgml4aUVJRmlSpPUS7JZCZksbLDL01kZCmWXOj0STgSjVpLgPqLFuqCndSD6twCTvSc3_D3yrMgb6Zn_It2kIpinHoVKJ5hWM0978xrgoB7oE2_Rc_jeZ-THH5qThiuF7CBop1pkGGXThY6IKjZQywzOFuNYCH_hPYHEQsPPNnto5KEO7Zh_Koy8LxTSZ33sMmpRIHAXG0iFYjwWRY784oYTJZfzmfq0oI0pz19qzVitsl16mfcxKsxdp_EM8bQbVEOk8frQZTWa04cbHVqIfOeO4FsIwuEAYHMyr7bzlh9YnFCGxy2BCdMeiEJzmFmD__ryorYWUJDpGy6P0NA"
    
    if (AuthToken == ""):
        # AuthToken ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMDIwMTIxMjE3NTUxOSIsImlzcyI6ImZpcmViYXNlLWFkbWluc2RrLW9wbjd2QGhvdGVsb3BzLThkZjk5LmlhbS5nc2VydmljZWFjY291bnQuY29tIiwic3ViIjoiZmlyZWJhc2UtYWRtaW5zZGstb3BuN3ZAaG90ZWxvcHMtOGRmOTkuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJhdWQiOiJodHRwczovL2lkZW50aXR5dG9vbGtpdC5nb29nbGVhcGlzLmNvbS9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsImV4cCI6MTY4MDI0Mjg2MCwiaWF0IjoxNjgwMjM5MjYwfQ.WiAu2T38b30AXta1_PHfgmuSrAVfe1FgPiQwMNzM2KZq7ODRqP1fr-J_xiHopMXaX50FO-Tnyeq6I1Oqoa_VCs54gaEGPFEjtqBQfp2qPgvYHg-clQBG647Zzmu3tAVvX3jeE-BpludwFjWXcNr7JkXr7nqetHWsThEMfwz01FztDM9dvd2Cvk17c4Z7pZ3QO7YFcpAbf069LVC_ymqvw86ZNFbkx2Tv4cCn1BlqB9KJGCiicd-uwBriG5ai-q5dBJLftNyK82PUL6Ixko5E1zEG78glx9KbNwnkLtZdCY8oKuifgO5dQthJqFc6KUxgk_JprsxbKsrHFj23K6t-mg"
        return redirect("https://hotelops.in")
    else:
        url = (

            "https://hotelops.in/api/HotelOpsMgmtPyAPI/UserLogin/?AuthToken="+AuthToken)

        response = requests.get(url)

        if response.status_code == 200:
        
            pRedirect = request.GET.get('p', "")
            data = response.json()
            # print("session data::",data)
          
            request.session["UserID"] = str(data["Table"][0]["UserID"])
            request.session["OrganizationName"] = str(
                data["Table"][0]["Organization_name"])
            request.session["DomainCode"] = str(data["Table"][0]["DomainCode"])
            request.session["EmployeeCode"]=str(data["Table"][0]["EmployeeCode"])
            request.session["OrganizationLogo"] = str(
                "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"+data["Table"][0]["OrganizationLogo"])
            request.session["FullName"] = str(data["Table1"][0]["FullName"])
            request.session["UserType"]=str(data["Table"][0]["UserType"])
            request.session["Department_Name"]=str(data["Table1"][0]["Department_Name"])
            request.session["OrganizationID"] = str(
                data["Table"][0]["OrganizationID"])
            request.session["Logout"] = "https://"+request.session["DomainCode"] + \
                "."+MasterAttribute.Logout+""+AuthToken
            request.session["HomeURL"] = "https://"+request.session["DomainCode"] + \
                "."+MasterAttribute.HomeURL+""+AuthToken
            
            request.session["ChangePassword"] = "https://"+request.session["DomainCode"] + \
                "."+MasterAttribute.ChangePassword+""+AuthToken
            request.session["MasterURL"] = "https://"+request.session["DomainCode"] + \
                ".hotelops.in/"
            ProductUserRightsList=str(data["Table"][0]["ProductUserRightsList"])
            cache.set('ProductUserRightsList', ProductUserRightsList, timeout=60*30)
            cache.set('AuthToken', AuthToken, timeout=60*30)
            user_session, created = UserSession.objects.update_or_create(
                user_id=request.session["UserID"],
                defaults={
                    'auth_token': "",
                    'session_key': request.session.session_key,
                    'organization_name': request.session["OrganizationName"],
                    'domain_code': request.session["DomainCode"],
                    'organization_logo': request.session["OrganizationLogo"],
                    'full_name': request.session["FullName"],
                    'employee_code': request.session["EmployeeCode"],
                    'level': "",
                    'department_name': request.session["Department_Name"],
                    'user_type': request.session["UserType"],
                    'organization_id': request.session["OrganizationID"]
                }
            )       
            request.session["ApiToken"] = GenerateToken(AuthToken)
            return redirect(pRedirect)
            # print(data["Table"][0]["UserID"])
            # print(data["Table"][0]["OrganizationID"])
            # print("---Session ")
            # print("User ID")
            # print(request.session["UserID"])
            # return redirect("/showpage/")

            # Do something with the data

        else:

            print(f"Error: {response.status_code} - {response.reason}")

    return render(request, 'apps/index.html')

from django.http import JsonResponse
def GenerateToken(AuthToken):
    print("GenerateToken")
    url = 'https://hotelops.in//API/PyModuleAuthAPI/GenerateToken'
    
    headers={
        'mobile-app-api-token':'cOwzYa08a1Z9rF4jwbylBiMmkvPym1sKVYau7lzRQgUTE3CtfgvQQ0I0KKWD58q28xpZHD6cE7rg3a2rbpLH1JqXYFRZopr346PFCgTdu8oe1SgcJBiSLGZxbcCgfvMm08by9mLc3vyTmX25ggX8jMAQxcQwxmg2kcZ4HZw1uI4Zo4TBTLwszOZyyo0Bb0HPJTBUEJ65wAIskDEKArKhRu3MLefqRDaebVjTopAfxkCyehLPSd3e0ct05Y'
    }
    
    try:
        response = requests.post(url,headers=headers, data={'AuthToken': AuthToken})
        if response.status_code == 200:
            data = response.json()
            print(f"Bearer {data['token']}")
            return  f"{data['token']}"
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
   
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache

@api_view(['GET'])
def get_cached_data(request):
    AuthToken = cache.get('AuthToken', '')
    # print("AuthToken:", AuthToken)

    AuthToken="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMDIyMTEwNTE2ODMwOCIsImlzcyI6ImZpcmViYXNlLWFkbWluc2RrLW9wbjd2QGhvdGVsb3BzLThkZjk5LmlhbS5nc2VydmljZWFjY291bnQuY29tIiwic3ViIjoiZmlyZWJhc2UtYWRtaW5zZGstb3BuN3ZAaG90ZWxvcHMtOGRmOTkuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJhdWQiOiJodHRwczovL2lkZW50aXR5dG9vbGtpdC5nb29nbGVhcGlzLmNvbS9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsImV4cCI6MTczNzYyMzAxNCwiaWF0IjoxNzM3NjE5NDE0fQ.Es0mgml4aUVJRmlSpPUS7JZCZksbLDL01kZCmWXOj0STgSjVpLgPqLFuqCndSD6twCTvSc3_D3yrMgb6Zn_It2kIpinHoVKJ5hWM0978xrgoB7oE2_Rc_jeZ-THH5qThiuF7CBop1pkGGXThY6IKjZQywzOFuNYCH_hPYHEQsPPNnto5KEO7Zh_Koy8LxTSZ33sMmpRIHAXG0iFYjwWRY784oYTJZfzmfq0oI0pz19qzVitsl16mfcxKsxdp_EM8bQbVEOk8frQZTWa04cbHVqIfOeO4FsIwuEAYHMyr7bzlh9YnFCGxy2BCdMeiEJzmFmD__ryorYWUJDpGy6P0NA"
    url = f"https://hotelops.in/api/userapi/ModuleList?id={AuthToken}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        
        # Use safe=False if data is not a dictionary
        return JsonResponse(data, safe=isinstance(data, dict))

    return JsonResponse({"error": "Failed to retrieve data"}, status=response.status_code)


@api_view(['GET'])
def getToken(request):
    # Retrieve data from the cache
    AuthToken = cache.get('AuthToken', None)

    if AuthToken is None:
       return JsonResponse({"message": "No data found in cache"}, status=404)
    
    return JsonResponse({"AuthToken": AuthToken})


def OrganizationList(OrganizationID):
    try:
        if OrganizationID == "3":
            organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1).values('OrganizationID', 'OrganizationName')
        else:
            organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID).values('OrganizationID', 'OrganizationName')
        return organizations
    except OrganizationMaster.DoesNotExist:
        
        return None
    except Exception as e:
       
        print(f"An error occurred: {e}")
        return None

def home_view(request):

    AuthToken = request.GET.get('AuthToken', "")
    if (AuthToken == ""):
        # AuthToken ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMDIwMTIxMjE3NTUxOSIsImlzcyI6ImZpcmViYXNlLWFkbWluc2RrLW9wbjd2QGhvdGVsb3BzLThkZjk5LmlhbS5nc2VydmljZWFjY291bnQuY29tIiwic3ViIjoiZmlyZWJhc2UtYWRtaW5zZGstb3BuN3ZAaG90ZWxvcHMtOGRmOTkuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJhdWQiOiJodHRwczovL2lkZW50aXR5dG9vbGtpdC5nb29nbGVhcGlzLmNvbS9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsImV4cCI6MTY4MDI0Mjg2MCwiaWF0IjoxNjgwMjM5MjYwfQ.WiAu2T38b30AXta1_PHfgmuSrAVfe1FgPiQwMNzM2KZq7ODRqP1fr-J_xiHopMXaX50FO-Tnyeq6I1Oqoa_VCs54gaEGPFEjtqBQfp2qPgvYHg-clQBG647Zzmu3tAVvX3jeE-BpludwFjWXcNr7JkXr7nqetHWsThEMfwz01FztDM9dvd2Cvk17c4Z7pZ3QO7YFcpAbf069LVC_ymqvw86ZNFbkx2Tv4cCn1BlqB9KJGCiicd-uwBriG5ai-q5dBJLftNyK82PUL6Ixko5E1zEG78glx9KbNwnkLtZdCY8oKuifgO5dQthJqFc6KUxgk_JprsxbKsrHFj23K6t-mg"
        return redirect("https://hotelops.in")
    else:
        url = (

            # "https://hotelops.in/api/HotelOpsMgmtPyAPI/UserLogin/?AuthToken="+AuthToken)
            "http://localhost:50970//api/HotelOpsMgmtPyAPI/UserLogin/?AuthToken="+AuthToken)

        response = requests.get(url)

        if response.status_code == 200:
            pRedirect = request.GET.get('p', "")
            data = response.json()
         
            request.session["UserID"] = str(data["Table"][0]["UserID"])
            request.session["OrganizationName"] = str(
                data["Table"][0]["Organization_name"])
            request.session["DomainCode"] = str(data["Table"][0]["DomainCode"])
            request.session["OrganizationLogo"] = str(
                "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"+data["Table"][0]["OrganizationLogo"])
            request.session["FullName"] = str(data["Table1"][0]["FullName"])
            request.session["EmployeeCode"]=str(data["Table"][0]["EmployeeCode"])
            request.session["Department_Name"]=str(data["Table1"][0]["Department_Name"])
            ProductUserRightsList=str(data["Table"][0]["ProductUserRightsList"])
            cache.set('ProductUserRightsList', ProductUserRightsList, timeout=60*30)
            cache.set('AuthToken', AuthToken, timeout=60*30)

            request.session["ProductUserRightsList"]=ProductUserRightsList;
            request.session["UserType"]=str(data["Table"][0]["UserType"])
            request.session["OrganizationID"] = str(
                data["Table"][0]["OrganizationID"])
            request.session["Logout"] = "https://"+request.session["DomainCode"] + \
                "."+MasterAttribute.Logout+""+AuthToken
            request.session["HomeURL"] = "https://"+request.session["DomainCode"] + \
                "."+MasterAttribute.HomeURL+""+AuthToken
            request.session["ChangePassword"] = "https://"+request.session["DomainCode"] + \
                "."+MasterAttribute.ChangePassword+""+AuthToken
            print("pRedirect--->")
            print(pRedirect)
            request.session["MasterURL"] = "https://"+request.session["DomainCode"] + \
                ".hotelops.in/"
            request.session["ApiToken"] = GenerateToken(AuthToken)
            defaults={
                    'auth_token': "",
                    'session_key': request.session.session_key,
                    'organization_name': request.session["OrganizationName"],
                    'domain_code': request.session["DomainCode"],
                    'organization_logo': request.session["OrganizationLogo"],
                    'full_name': request.session["FullName"],
                    'employee_code': request.session["EmployeeCode"],
                    'level': "",
                    'department_name': request.session["Department_Name"],
                    'user_type': request.session["UserType"],
                    'organization_id': request.session["OrganizationID"]
                }
            return redirect(pRedirect)
            # print(data["Table"][0]["UserID"])
            # print(data["Table"][0]["OrganizationID"])
            # print("---Session ")
            # print("User ID")
            # print(request.session["UserID"])
            # return redirect("/showpage/")

            # Do something with the data

        else:

            print(f"Error: {response.status_code} - {response.reason}")

    return render(request, 'apps/index.html')

# Inserting Cake Order Form

from django.db  import connection, transaction


from .models import UserSession,City_Location_Master
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.db import connection
def LoginPage(request):
    AuthToken = request.GET.get('AuthToken', "")
    error_message = None  
    if request.method == 'POST':
        domain_code = request.POST.get('domainCode')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            cursor.execute(
                "EXEC Py_SP_HTL_User_Login @DomainCode=%s, @Username=%s, @Password=%s",
                [domain_code, username, password]
            )
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        
        rowslist = [dict(zip(columns, row)) for row in rows]
        
        if rowslist:
            data = rowslist[0]
            
            # Save session details
            request.session["UserID"] = str(data.get("UserID", ""))
            request.session.save()  
            
            request.session["session_key"] = request.session.session_key
            request.session["OrganizationName"] = str(data.get("Organization_name", ""))
            request.session["DomainCode"] = str(data.get("DomainCode", ""))
            request.session["OrganizationLogo"] = str(
                "https://hotelopsblob.blob.core.windows.net/hotelopslogos/" + data.get("OrganizationLogo", "")
            )
            request.session["FullName"] = str(data.get("FullName", ""))
            request.session["EmployeeCode"] = str(data.get("EmployeeCode", ""))
            request.session["Level"] = str(data.get("Level", ""))
            request.session["Department_Name"] = str(data.get("Department_Name", ""))
            request.session["UserType"] = str(data.get("UserType", ""))
            request.session["OrganizationID"] = str(data.get("OrganizationID", ""))
            
            
            # token, created = Token.objects.get_or_create(user_id=request.session["UserID"])
            request.session["AuthToken"] = ""
            request.session["ApiToken"]=""
            
            
            user_session, created = UserSession.objects.update_or_create(
                user_id=request.session["UserID"],
                defaults={
                    'auth_token': request.session["AuthToken"],
                    'session_key': request.session.session_key,
                    'organization_name': request.session["OrganizationName"],
                    'domain_code': request.session["DomainCode"],
                    'organization_logo': request.session["OrganizationLogo"],
                    'full_name': request.session["FullName"],
                    'employee_code': request.session["EmployeeCode"],
                    'level': request.session["Level"],
                    'department_name': request.session["Department_Name"],
                    'user_type': request.session["UserType"],
                    'organization_id': request.session["OrganizationID"]
                }
            )
            
            pRedirect = request.GET.get('p', '')
            return redirect(pRedirect if pRedirect else 'Dashboard')
        else:
            error_message = "Invalid domain code, username, or password. Please try again."

    return render(request, 'apps/LoginPage.html', {'error_message': error_message})
   
def OrganizationLogo(OrganizationID):
    if OrganizationID:
        org  =OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1,OrganizationID=OrganizationID).values('OrganizationID', 'OrganizationLogo').first()
        if org:
            orgLogo  = org['OrganizationLogo']
            return orgLogo
    else:
         return None       
    
def EmployeeDataSelect(OrganizationID=None, EmployeeCode=None,Designation =None,ReportingtoDesignation =None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EmployeeMaster_Select_Data @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s", [OrganizationID, EmployeeCode,Designation,ReportingtoDesignation])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist

def EmployeeDataSelectLeaveCredit_Data(OrganizationID=None, EmployeeCode=None,Designation =None,ReportingtoDesignation =None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EmployeeMaster_LeaveCredit_Data @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s", [OrganizationID, EmployeeCode,Designation,ReportingtoDesignation])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist


def OrganizationName(OrganizationID):
    if OrganizationID:
        org  =OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1,OrganizationID=OrganizationID).values('OrganizationID', 'OrganizationName').first()
        if org:
            orgName  = org['OrganizationName']
            return orgName
    else:
         return None    




from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def logout_view(request):
    auth_logout(request)
    return redirect('LoginPage')



from hotelopsmgmtpy.utils import encrypt_id,decrypt_id
def Dashboard(request):
    #return redirect(request.session.get("HomeURL"))
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    SessionUserID = str(request.session["UserID"])
    UserID=encrypt_id(SessionUserID)
    return render(request, 'apps/Dashboard.html',{'UserID':UserID})

def Error(request, message):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
 
    context = {'message': message}
    return render(request, 'apps/Error.html', context)

from django.http import JsonResponse
from rest_framework import status
def GetEmployeeDetails(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session.get("OrganizationID")
    EmployeeCode = request.GET.get('EmployeeCode')
    
    if OrganizationID and EmployeeCode:
        try:
            obj = EmployeeMaster.objects.get(EmployeeCode=EmployeeCode, OrganizationID=OrganizationID, IsDelete=False)
            EmployeeData = {
                'EmployeeCode': obj.EmployeeCode,
                'EmpName': obj.EmpName,
                'Department': obj.Department,
                'Designation': obj.Designation,
                'DateofJoining': obj.DateofJoining,
                'ReportingtoDesigantion': obj.ReportingtoDesigantion,
                'ReportingtoLevel': obj.ReportingtoLevel,
                'Level': obj.Level,
                'EmpStatus': obj.EmpStatus,
                'Gender': obj.Gender,
                'DOB':obj.DOB,
                'BloodGroup':obj.BloodGroup,
                'EmergencyContact':obj.EmergencyContact
            }
            return JsonResponse(EmployeeData, safe=False, status=status.HTTP_200_OK)
        except EmployeeMaster.DoesNotExist:
            return JsonResponse({"error": "No Records exist"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({"error": "Invalid request parameters"}, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from rest_framework import status
from django.db import connection

def GetEmployeeDetailsApi(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)

    OrganizationID = request.GET.get('OID')
    EmployeeCode = request.GET.get('EmployeeCode')

    if not OrganizationID or not EmployeeCode:
        return JsonResponse({"error": "OrganizationID and EmployeeCode are required parameters"}, status=status.HTTP_400_BAD_REQUEST)
    
    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC SP_EmployeeMaster_Select_Data @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s",
            [OrganizationID, EmployeeCode, None, None]
        )
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    rowslist = [dict(zip(columns, row)) for row in rows]
    return JsonResponse(rowslist, safe=False)




def EmployeeUserLoginTokenMobile(OrganizationID=None, EmployeeCode=None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_UserLoginFcmToken_Select @OrganizationID=%s, @EmployeeCode=%s", [OrganizationID, EmployeeCode])

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist


def HOD_Details(OrganizationID, Department,Level):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EmployeeMaster_HOD_FcmTokenSelect @OrganizationID=%s, @Department=%s,@Level=%s", [OrganizationID,Department, Level])

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist


def EmployeeDataSelectForSalary(OrganizationID=None, Month =None,Year=None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC [SP_EmployeeMaster_Select_Data_For_Salary_demo] @OrganizationID=%s, @Month=%s, @Year=%s", [OrganizationID, Month,Year])
        # cursor.execute("EXEC SP_EmployeeMaster_Select_Data_For_Salary @OrganizationID=%s, @Month=%s, @Year=%s", [OrganizationID, Month,Year])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist