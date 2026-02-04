from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
from app.models import EmployeeMaster
from .models import ItInformation,SimDetail,SystemDetail,EmailDetail,MobileDetail
from django.db import transaction
from django.contrib import messages
from  django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status




from HumanResources.views import DepartmentofEmployee,get_employee_designation_by_EmployeeCode
def ItManagerList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    EmployeeCode = request.session["EmployeeCode"]
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    ReportingtoDesignation = get_employee_designation_by_EmployeeCode(OrganizationID,EmployeeCode)
   
  
    ITM = False
   
    if EmployeeCode:
        Repobj = DepartmentofEmployee(request, OrganizationID, EmployeeCode)
        print("Repobj = ",Repobj)
        if Repobj:
            work_Department = Repobj.get('work_Department')

            if 'IT' in work_Department :
                ITM = True
    if ITM:
   
   
        its = ItInformation.objects.filter(OrganizationID=OrganizationID, IsDelete=False,  HodStatus=1,
                HrStatus=1,).order_by('-id')

        # Prepare context with is_issued information
        its_with_issued_status = []
        for it in its:
            it.Rights = "ITM"
            it.save()

            sim_issued = SimDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
            mobile_issued = MobileDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
            email_issued = EmailDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
            system_issued = SystemDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
            
            its_with_issued_status.append({
                'it': it,
                'sim_issued': 'Issued' if sim_issued else 'Not Issued',
                'mobile_issued': 'Issued' if mobile_issued else 'Not Issued',
                'email_issued': 'Issued' if email_issued else 'Not Issued',
                'system_issued': 'Issued' if system_issued else 'Not Issued',
            })
    
    else:
        its = ItInformation.objects.filter(OrganizationID=OrganizationID, IsDelete=False,ReportingtoDesigantion=ReportingtoDesignation,
                                            HrStatus=1,
                HodStatus = 0).order_by('-id')

        # Prepare context with is_issued information
        its_with_issued_status = []
        for it in its:
            it.Rights = "REP"
            it.save()

            sim_issued = SimDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
            mobile_issued = MobileDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
            email_issued = EmailDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
            system_issued = SystemDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
            
            its_with_issued_status.append({
                'it': it,
                'sim_issued': 'Issued' if sim_issued else 'Not Issued',
                'mobile_issued': 'Issued' if mobile_issued else 'Not Issued',
                'email_issued': 'Issued' if email_issued else 'Not Issued',
                'system_issued': 'Issued' if system_issued else 'Not Issued',
            })

    

   

    context = {'ITS': its_with_issued_status,
                'hotelapitoken': hotelapitoken,
                'ReportingtoDesigantion': ReportingtoDesignation,
                'UserID': UserID,
                'OrganizationID': OrganizationID
    }
    return render(request, "ITM/ItManagerList.html", context)



# Hr Request


from django.urls import reverse
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeNameandDesignation
@transaction.atomic()
def  HrRequest(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID    
    RequestedBy =   request.session["FullName"] 
    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    EmpCode = request.GET.get('EC')
    EmpID = request.GET.get('EmpID')
  
    ID  =  request.GET.get('ITID')
   
    
    ITS = None
    SI  = None
    MB = None
    SYS  = None
    EM = None

    
    if EmpCode is not None:
        if ID is not None:
            ITS = ItInformation.objects.filter(OrganizationID=OrganizationID, IsDelete=False, id=ID).first()

        if ITS is not None:
            print("Inside ITS ")
            DataFromITobj = 'DataFromITobj'
        else:
            DataFromITobj = 'DataFromITobjHR'
            EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)

            ITS = {
                'EmployeeCode': EmpDetails.EmployeeCode,
                'EmployeeName': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
                'Department': EmpDetails.Department,
                'DesignationGrade': EmpDetails.Designation,
                'ReportingtoDesigantion': EmpDetails.ReportingtoDesignation
            }
        if DataFromITobj == 'DataFromITobj' :
            print("Inside SI")
            SI = SimDetail.objects.filter(ItInformation=ITS, OrganizationID=OrganizationID, IsDelete=False).first()
            MB = MobileDetail.objects.filter(ItInformation=ITS, OrganizationID=OrganizationID, IsDelete=False).first()
            SYS = SystemDetail.objects.filter(ItInformation=ITS, OrganizationID=OrganizationID, IsDelete=False).first()
            EM = EmailDetail.objects.filter(ItInformation=ITS, OrganizationID=OrganizationID, IsDelete=False).first()

    with transaction.atomic():
        if request.method == "POST":
            EmployeeCode = request.POST['EmpCode']

            if DataFromITobj == "DataFromITobj" and ID:
                ITS.ModifyBy = UserID
                ITS.save()

                IsSim = request.POST.get('simCheckbox', None)
                if IsSim == 'Sim':
                    DateofRequest_Sim = request.POST['DateofRequest_Sim']
                    Sim = SimDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False, ItInformation__EmployeeCode=EmployeeCode).first()
                    if Sim is None:
                        Sim = SimDetail.objects.create(
                            ItInformation=ITS,
                            DateofRequest=DateofRequest_Sim,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                            RequestedBy=RequestedBy
                        )
                        ITS.HodStatus = 0
                        ITS.save()

                IsMobile = request.POST.get('mobileCheckbox', None)
                if IsMobile == 'Mobile':
                    DateofRequest_Mob = request.POST['DateofRequest_Mob']
                    Mobile = MobileDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False, ItInformation__EmployeeCode=EmployeeCode).first()
                    if Mobile is None:
                        Mobile = MobileDetail.objects.create(
                            ItInformation=ITS,
                            DateofRequest=DateofRequest_Mob,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                            RequestedBy=RequestedBy
                        )
                        ITS.HodStatus = 0
                        ITS.save()

                IsEmail = request.POST.get('emailCheckbox', None)
                if IsEmail == 'Email':
                    DateofRequest_Em = request.POST['DateofRequest_Em']
                    Email = EmailDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False, ItInformation__EmployeeCode=EmployeeCode).first()
                    if Email is None:
                        Email = EmailDetail.objects.create(
                            ItInformation=ITS,
                            DateofRequest=DateofRequest_Em,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                            RequestedBy=RequestedBy
                        )
                        ITS.HodStatus = 0
                        ITS.save()

                IsSystem = request.POST.get('sytstemCheckbox', None)
                if IsSystem == 'Sytstem':
                    DateofRequest_Sys = request.POST['DateofRequest_Sys']
                    System = SystemDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False, ItInformation__EmployeeCode=EmployeeCode).first()
                    if System is None:
                        System = SystemDetail.objects.create(
                            ItInformation=ITS,
                            DateofRequest=DateofRequest_Sys,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                            RequestedBy=RequestedBy
                        )
                        ITS.HodStatus = 0
                        ITS.save()


             

             



                
              

            else:
                print("In side else")
                EmployeeName = request.POST['EmployeeName'] or ''
                EmployeeCode = request.POST['EmpCode'] or ''
                DesignationGrade = request.POST['DesignationGrade'] or ''
                Department = request.POST['Department'] or ''
                ReportingtoDesigantion = request.POST['ReportingtoDesigantion']

                it = ItInformation.objects.filter(OrganizationID=OrganizationID, IsDelete=False, EmployeeCode=EmployeeCode).first()
                if it is None:
                    print("Insdie except")
                    it = ItInformation.objects.create(
                        EmployeeName=EmployeeName,
                        EmployeeCode=EmployeeCode,
                        DesignationGrade=DesignationGrade,
                        Department=Department,
                        OrganizationID=OrganizationID,
                        ReportingtoDesigantion=ReportingtoDesigantion,
                        CreatedBy=UserID,
                        HrStatus=1,
                        HodStatus=0,
                        ItStatus=0
                    )

                IsSim = request.POST.get('simCheckbox', None)
                if IsSim == 'Sim':
                    DateofRequest_Sim = request.POST['DateofRequest_Sim']
                    Sim = SimDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False, ItInformation__EmployeeCode=EmployeeCode).first()
                    if Sim is None:
                        Sim = SimDetail.objects.create(
                            ItInformation=it,
                            DateofRequest=DateofRequest_Sim,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                            RequestedBy=RequestedBy
                        )

                IsMobile = request.POST.get('mobileCheckbox', None)
                if IsMobile == 'Mobile':
                    DateofRequest_Mob = request.POST['DateofRequest_Mob']
                    Mobile = MobileDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False, ItInformation__EmployeeCode=EmployeeCode).first()
                    if Mobile is None:
                        Mobile = MobileDetail.objects.create(
                            ItInformation=it,
                            DateofRequest=DateofRequest_Mob,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                            RequestedBy=RequestedBy
                        )

                IsEmail = request.POST.get('emailCheckbox', None)
                if IsEmail == 'Email':
                    DateofRequest_Em = request.POST['DateofRequest_Em']
                    Email = EmailDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False, ItInformation__EmployeeCode=EmployeeCode).first()
                    if Email is None:
                        Email = EmailDetail.objects.create(
                            ItInformation=it,
                            DateofRequest=DateofRequest_Em,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                            RequestedBy=RequestedBy
                        )

                IsSystem = request.POST.get('sytstemCheckbox', None)
                if IsSystem == 'Sytstem':
                    DateofRequest_Sys = request.POST['DateofRequest_Sys']
                    System = SystemDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False, ItInformation__EmployeeCode=EmployeeCode).first()
                    if System is None:
                        System = SystemDetail.objects.create(
                            ItInformation=it,
                            DateofRequest=DateofRequest_Sys,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                            RequestedBy=RequestedBy
                        )

                
                            
                # SendITNotificationHOD(EmployeeCode, OrganizationID, UserID)

               
            
            
            
          
            Success = True        
            encrypted_id = encrypt_id(EmpID)
            url = reverse('IT')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
            return redirect(redirect_url)     


    context = {'OrganizationID':OrganizationID,'hotelapitoken':hotelapitoken,'ITS':ITS,'EM':EM,'SYS':SYS,'SI':SI,'MB':MB}
    return render(request,"ITM/HrRequest.html",context)









# @transaction.atomic()
# def  ITRequest(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
     
#     OrganizationID = request.session["OrganizationID"]
#     OID  = request.GET.get('OID')
#     if OID:
#             OrganizationID= OID   
             
#     RequestedBy =   request.session["FullName"] 
#     UserID = str(request.session["UserID"])
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken 
    
#     ID  =  request.GET.get('ID')
#     ITS = None
#     SI  = None
#     MB = None
#     SYS  = None
#     EM = None

#     if ID is not None:
#         ITS = get_object_or_404(ItInformation,OrganizationID=OrganizationID,IsDelete = False,id=ID)
#         try:
#             SI  = get_object_or_404(SimDetail,ItInformation=ITS,OrganizationID=OrganizationID,IsDelete = False)
#         except:
#             SI = None

#         try:
#             MB = get_object_or_404(MobileDetail,ItInformation=ITS,OrganizationID=OrganizationID,IsDelete = False)
#         except:
#             MB = None
#         try:
#             SYS = get_object_or_404(SystemDetail,ItInformation=ITS,OrganizationID=OrganizationID,IsDelete = False) 
#         except:
#             SYS = None
#         try:
#             EM = get_object_or_404(EmailDetail,ItInformation=ITS,OrganizationID=OrganizationID,IsDelete = False) 
#         except:
#             EM = None
            
#     with transaction.atomic():
#         if request.method == "POST":
#             if ID is not None:
#                 ITS.ModifyBy =  UserID
#                 ITS.ItStatus = 1
#                 ITS.save()
#                 if SI:
#                     SI.DateofIssue = request.POST.get('DateofIssue_Sim', None)
#                     SI.MobileNo = request.POST.get('MobileNo', '')
#                     SI.IsIssued = True
#                     SI.ModifyBy = UserID
#                     SI.save()
#                 if MB:
#                     MB.DateofIssue = request.POST.get('DateofIssue_Mob', None)
#                     MB.CompanyName = request.POST.get('CompanyName_Mob', '')
#                     MB.ModelNumber = request.POST.get('ModelNumber_Mob', '')
#                     MB.IMEINumber = request.POST.get('IMEINumber', '')
#                     MB.Colour = request.POST.get('Colour', '')
#                     MB.IsIssued = True
#                     MB.ModifyBy = UserID
#                     MB.save()
#                 if EM:    
#                     EM.DateofIssue = request.POST.get('DateofIssue_Em', None)
#                     EM.Email = request.POST.get('Email', '')
#                     EM.Type = request.POST.get('Type', '')
#                     EM.DomainType = request.POST.get('DoaminType', '')
#                     EM.IsIssued = True
#                     EM.ModifyBy = UserID
#                     EM.save()
#                 if SYS:    
#                     SYS.DateofIssue = request.POST.get('DateofIssue_Sys', None)
#                     SYS.SystemType = request.POST.get('SystemType', '')
#                     SYS.CompanyName = request.POST.get('CompanyName_Sys', '')
#                     SYS.ModelNumber = request.POST.get('ModelNumber_Sys', '')
#                     SYS.SerialNumber = request.POST.get('SerialNumber', '')
#                     SYS.Configuration = request.POST.get('Configuration', '')
#                     SYS.IsIssued  = True
#                     SYS.ModifyBy = UserID
#                     SYS.save()
                    
#                 messages.success(request,"Aprroved Successfully")

#             return redirect('ItManagerList') 

#     context = {
#         'OrganizationID':OrganizationID,
#         'hotelapitoken':hotelapitoken,
#         'ITS':ITS,
#         'EM':EM,
#         'SYS':SYS,
#         'SI':SI,
#         'MB':MB
#     }
#     return render(request,"ITM/ITRequest.html",context)





# @transaction.atomic()
# def  ITRequest(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
     
#     OrganizationID = request.session["OrganizationID"]
#     OID  = request.GET.get('OID')
#     if OID:
#             OrganizationID= OID   
             
#     RequestedBy =   request.session["FullName"] 
#     UserID = str(request.session["UserID"])
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken 
    
#     ID  =  request.GET.get('ID')
#     ITS = None
#     SI  = None
#     MB = None
#     SYS  = None
#     EM = None

#     if ID is not None:
#         ITS = get_object_or_404(ItInformation,OrganizationID=OrganizationID,IsDelete = False,id=ID)
#         try:
#             SI  = get_object_or_404(SimDetail,ItInformation=ITS,OrganizationID=OrganizationID,IsDelete = False)
#         except:
#             SI = None

#         try:
#             MB = get_object_or_404(MobileDetail,ItInformation=ITS,OrganizationID=OrganizationID,IsDelete = False)
#         except:
#             MB = None
#         try:
#             SYS = get_object_or_404(SystemDetail,ItInformation=ITS,OrganizationID=OrganizationID,IsDelete = False) 
#         except:
#             SYS = None
#         try:
#             EM = get_object_or_404(EmailDetail,ItInformation=ITS,OrganizationID=OrganizationID,IsDelete = False) 
#         except:
#             EM = None
            
#     with transaction.atomic():
#         if request.method == "POST":
#             if ID is not None:
#                 ITS.ModifyBy =  UserID
#                 ITS.ItStatus = 1
#                 ITS.save()
#                 if SI:
#                     SI.DateofIssue = request.POST.get('DateofIssue_Sim', None)
#                     SI.MobileNo = request.POST.get('MobileNo', '')
#                     SI.IsIssued = True
#                     SI.ModifyBy = UserID
#                     SI.save()
#                 if MB:
#                     MB.DateofIssue = request.POST.get('DateofIssue_Mob', None)
#                     MB.CompanyName = request.POST.get('CompanyName_Mob', '')
#                     MB.ModelNumber = request.POST.get('ModelNumber_Mob', '')
#                     MB.IMEINumber = request.POST.get('IMEINumber', '')
#                     MB.Colour = request.POST.get('Colour', '')
#                     MB.IsIssued = True
#                     MB.ModifyBy = UserID
#                     MB.save()
#                 if EM:    
#                     EM.DateofIssue = request.POST.get('DateofIssue_Em', None)
#                     EM.Email = request.POST.get('Email', '')
#                     EM.Type = request.POST.get('Type', '')
#                     EM.DomainType = request.POST.get('DoaminType', '')
#                     EM.IsIssued = True
#                     EM.ModifyBy = UserID
#                     EM.save()
#                 if SYS:    
#                     SYS.DateofIssue = request.POST.get('DateofIssue_Sys', None)
#                     SYS.SystemType = request.POST.get('SystemType', '')
#                     SYS.CompanyName = request.POST.get('CompanyName_Sys', '')
#                     SYS.ModelNumber = request.POST.get('ModelNumber_Sys', '')
#                     SYS.SerialNumber = request.POST.get('SerialNumber', '')
#                     SYS.Configuration = request.POST.get('Configuration', '')
#                     SYS.IsIssued  = True
#                     SYS.ModifyBy = UserID
#                     SYS.save()
                    
#                 messages.success(request,"Aprroved Successfully")

#             return redirect('ItManagerList') 

#     context = {
#         'OrganizationID':OrganizationID,
#         'hotelapitoken':hotelapitoken,
#         'ITS':ITS,
#         'EM':EM,
#         'SYS':SYS,
#         'SI':SI,
#         'MB':MB
#     }
#     return render(request,"ITM/ITRequest.html",context)

from app.Global_Api import Get_Employee_Master_Data_By_Code
from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail
from django.utils import timezone
from Checklist_Issued.views import run_background_checklist_tasks

@transaction.atomic
def ITRequest(request):
    # Validate session
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    OID = request.GET.get("OID")
    if OID:
        OrganizationID = int(OID)

    RequestedBy = request.session["FullName"]
    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken

    # Check for ID (existing record → not allowed)
    EmployeeCode = request.GET.get("EC")
    Hide = request.GET.get("Hide")
    ID = request.GET.get("ID")

    Hide_Value=False
    if Hide:
        Hide_Value = Hide
        
    EmployeeData=None  
    if EmployeeCode:
        EmployeeData = Get_Employee_Master_Data_By_Code(EmployeeCode,OID)
        
        
    # print("Employee Data is here::", EmployeeData   )
    

    # If ID exists → block update
    if ID:
        messages.error(request, "Updating existing IT Request is not allowed.")
        return redirect("ItManagerList")

    # Render blank form on GET
    if request.method == "GET":
        return render(request, "ITM/ITRequest.html", {
            "OrganizationID": OrganizationID,
            "hotelapitoken": hotelapitoken,
            'EmployeeData': EmployeeData, 
            'RequestedBy': RequestedBy, 
            "ITS": None,
            "SI": None,
            "MB": None,
            "SYS": None,
            "EM": None
        })

    # ------------------------------
    #        CREATE NEW RECORD
    # ------------------------------

    if request.method == "POST":
        # User_OrganizationID=request.POST.get("OrganizationID")
        User_OID=int(OID)
        

        # Create IT Information
        ITS = ItInformation.objects.create(
            EmployeeName = request.POST.get("EmployeeName"),
            EmployeeCode = request.POST.get("EmpCode"),
            DesignationGrade = request.POST.get("DesignationGrade"),
            Department = request.POST.get("Department"),
            ReportingtoDesigantion = request.POST.get("ReportingtoDesigantion"),
            HotelOpsAccount = request.POST.get("HotelOpsAccount"),
            OrganizationID=User_OID,
            ItStatus=1,
            CreatedBy=UserID,
            IsDelete=False
        )

        # Create SIM Detail (only if fields exist)
        if request.POST.get("MobileNo"):
            SimDetail.objects.create(
                ItInformation=ITS,
                DateofIssue=request.POST.get("DateofIssue_Sim"),
                MobileNo=request.POST.get("MobileNo"),
                RequestedBy=request.POST.get("RequestedBy_Sim"),
                OrganizationID=User_OID,
                IsIssued=True,
                CreatedBy=UserID
            )
            Object_sim = 15
            run_background_checklist_tasks(EmployeeCode,OID, Object_sim, UserID)

        # Create Mobile Detail
        if request.POST.get("ModelNumber_Mob"):
            MobileDetail.objects.create(
                ItInformation=ITS,
                DateofIssue=request.POST.get("DateofIssue_Mob"),
                CompanyName=request.POST.get("CompanyName_Mob"),
                ModelNumber=request.POST.get("ModelNumber_Mob"),
                IMEINumber=request.POST.get("IMEINumber"),
                RequestedBy=request.POST.get("RequestedBy_Mob"),
                Colour=request.POST.get("Colour"),
                OrganizationID=User_OID,
                IsIssued=True,
                CreatedBy=UserID
            )
            Object_Mob = 14
            run_background_checklist_tasks(EmployeeCode,OID, Object_Mob, UserID)

        # Create Email Detail
        if request.POST.get("Email"):
            EmailDetail.objects.create(
                ItInformation=ITS,
                DateofIssue=request.POST.get("DateofIssue_Em"),
                Email=request.POST.get("Email"),
                Type=request.POST.get("Type"),
                DomainType=request.POST.get("DoaminType"),
                RequestedBy=request.POST.get("RequestedBy_EM"),
                OrganizationID=User_OID,
                IsIssued=True,
                CreatedBy=UserID
            )
            Object_Email = 5
            run_background_checklist_tasks(EmployeeCode,OID, Object_Email, UserID)

        # Create System Detail
        if request.POST.get("SerialNumber"):
            SystemDetail.objects.create(
                ItInformation=ITS,
                DateofIssue=request.POST.get("DateofIssue_Sys"),
                SystemType=request.POST.get("SystemType"),
                CompanyName=request.POST.get("CompanyName_Sys"),
                ModelNumber=request.POST.get("ModelNumber_Sys"),
                SerialNumber=request.POST.get("SerialNumber"),
                Configuration=request.POST.get("Configuration"),
                RequestedBy=request.POST.get("RequestedBy_SYS"),
                OrganizationID=User_OID,
                IsIssued=True,
                CreatedBy=UserID
            )
            Object_System = 20
            run_background_checklist_tasks(EmployeeCode,OID, Object_System, UserID)
            
        # 4. Update LOA table
        AppointemetLetters = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
            OrganizationID=OID, IsDelete=False, emp_code=EmployeeCode
        )

        AppointemetLetters.update(
            IT=True,
            ITCreatedBy=UserID,
            ITCreatedDateTime=timezone.now()
        )
        Object_ID = 67
        run_background_checklist_tasks(EmployeeCode,OID, Object_ID, UserID)
        messages.success(request, "New IT Request Created Successfully")
        return redirect("Issue_view")


    context = {
        'OrganizationID':OrganizationID,
        'hotelapitoken':hotelapitoken,
        'ITS':ITS,
        'EmployeeData': EmployeeData, 
    }
    return render(request,"ITM/ITRequest.html",context)



def ITRequest_ViewOnly(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
        OrganizationID = OID

    ID = request.GET.get('ID')

    ITS = None
    SI = None
    MB = None
    SYS = None
    EM = None

    # Load Main IT Information Record
    if ID is not None:
        ITS = get_object_or_404(
            ItInformation,
            OrganizationID=OrganizationID,
            IsDelete=False,
            id=ID
        )

        # Try loading related objects (if available)
        try:
            SI = SimDetail.objects.get(
                ItInformation=ITS,
                OrganizationID=OrganizationID,
                IsDelete=False
            )
        except:
            SI = None

        try:
            MB = MobileDetail.objects.get(
                ItInformation=ITS,
                OrganizationID=OrganizationID,
                IsDelete=False
            )
        except:
            MB = None

        try:
            SYS = SystemDetail.objects.get(
                ItInformation=ITS,
                OrganizationID=OrganizationID,
                IsDelete=False
            )
        except:
            SYS = None

        try:
            EM = EmailDetail.objects.get(
                ItInformation=ITS,
                OrganizationID=OrganizationID,
                IsDelete=False
            )
        except:
            EM = None

    context = {
        "OrganizationID": OrganizationID,
        "ITS": ITS,
        "SI": SI,
        "MB": MB,
        "SYS": SYS,
        "EM": EM,
        "view_only": True  # optional flag for template
    }

    return render(request, "ITM/ITRequest_ViewOnly.html", context)


@transaction.atomic
def  DeleteIT(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID    
     UserID = str(request.session["UserID"])
     id = request.GET.get('ID')
     with transaction.atomic():
        ITS = ItInformation.objects.get(id = id)
        ITS.IsDelete = True
        ITS.ModifyBy =  UserID
        ITS.save()
        
        SI = SimDetail.objects.get(ItInformation = ITS )
        SI.IsDelete = True
        SI.ModifyBy =  UserID
        SI.save()

        MB = MobileDetail.objects.get(ItInformation = ITS )
        MB.IsDelete = True
        MB.ModifyBy =  UserID
        MB.save()

        SYS = SystemDetail.objects.get(ItInformation = ITS )
        SYS.IsDelete = True
        SYS.ModifyBy =  UserID
        SYS.save()

        EM = EmailDetail.objects.get(ItInformation = ITS )
        EM.IsDelete = True
        EM.ModifyBy =  UserID
        EM.save()
        # Success = True        
        # encrypted_id = encrypt_id(EmpID)
        # url = reverse('IT')  
        # redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        # return redirect(redirect_url)    
        
        
  
from rest_framework.decorators import api_view

@api_view(['GET'])
def ItHodApprovalListApi(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
    
    OrganizationID = request.query_params.get('OrganizationID')
    ReportingtoDesignation = request.query_params.get('Designation')
    UserID = request.query_params.get('UserID')
   
    if OrganizationID and ReportingtoDesignation and UserID:
        employee_it_details = ItInformation.objects.filter(
            ReportingtoDesigantion=ReportingtoDesignation, 
            OrganizationID=OrganizationID,
            IsDelete=False
        )
        
        if not employee_it_details.exists():
            return JsonResponse({"error": "Employee IT details not found"}, status=status.HTTP_404_NOT_FOUND)
        
      
        employee_data = [
            {
                "ID":emp.id,
                "EmployeeName": emp.EmployeeName,
                "EmployeeCode": emp.EmployeeCode,
                "DesignationGrade": emp.DesignationGrade,
                "Department": emp.Department,
                
                "HodStatus": emp.HodStatus,
                "HodComment": emp.HodComment,
                "ReportingtoDesigantion": emp.ReportingtoDesigantion,
                "OrganizationID": emp.OrganizationID
            }
            for emp in employee_it_details
        ]
        
        return JsonResponse(employee_data, safe=False, status=status.HTTP_200_OK)
    
    return JsonResponse({"error": "Invalid parameters: OrganizationID, ReportingtoDesignation, or UserID"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def ITHodApprovalApi(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
    
    ID = request.data.get('ID')
    OrganizationID = request.data.get('OrganizationID') 
    UserID = request.data.get('UserID')
    HodStatus = request.data.get('HodStatus')
    HodComment = request.data.get('HodComment')
    
    if ID and UserID and HodStatus is not None and HodComment:
        try:
            employee_it_detail = ItInformation.objects.get(id=ID,IsDelete=False,OrganizationID =OrganizationID)
            
            if int(HodStatus) not in [1, -1]:
                return JsonResponse({"error": "Invalid status value. Use 1 for approve, -1 for reject."}, status=status.HTTP_400_BAD_REQUEST)
            
            employee_it_detail.HodStatus = HodStatus
            employee_it_detail.HodComment = HodComment
            employee_it_detail.save()
            if str(HodStatus) == '1':
                return JsonResponse({"success": "Approved successfully"}, status=200)
            elif str(HodStatus) == '-1':
                return JsonResponse({"success": "Rejected successfully"}, status=200)

        except ItInformation.DoesNotExist:
            return JsonResponse({"error": "Employee IT detail not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid parameters: ID, UserID, OrganizationID, or HodComment"}, status=400)




import requests
def SendITNotification(EmployeeCode, OrganizationID, UserID):
    url = "http://127.0.0.1:8000/EmailNotification/EmployeeITRequest/"
    hotel_api_token = MasterAttribute.HotelAPIkeyToken  
    headers = {
        "hotel-api-token": hotel_api_token,
        "Content-Type": "application/json"
    }
    payload = {
        "EmployeeCode": EmployeeCode,
        "OrganizationID": OrganizationID,
        "UserID": UserID
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")





import requests
def SendITNotificationHOD(EmployeeCode, OrganizationID, UserID):
    url = "http://127.0.0.1:8000/EmailNotification/EmployeeITRequestHOD/"
    hotel_api_token = MasterAttribute.HotelAPIkeyToken  
    headers = {
        "hotel-api-token": hotel_api_token,
        "Content-Type": "application/json"
    }
    payload = {
        "EmployeeCode": EmployeeCode,
        "OrganizationID": OrganizationID,
        "UserID": UserID
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")



