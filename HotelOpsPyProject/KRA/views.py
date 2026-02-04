from django.shortcuts import render,redirect
from app.models import OrganizationMaster
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from app.views import OrganizationList,OrganizationName
from HumanResources.views import TargetAssignNames,get_employee_designation_by_EmployeeCode,get_employee_names_by_designation,get_employee_name_designation_by_EmployeeCode,TargetAssignNamesWithReportingtoDesignationEmployeeNameCode, get_employee_name_by_code, TargetAssignNamesWithReportingtoDesignationEmployeeNameCode_New
from django.shortcuts import render, redirect
from .models import KRA, HotelKRAStandard, TargetAssignMaster, TargetAssignMasterDetails,KraEntryMaster,KraEntryMasterDetails
from datetime import date, datetime
from django.urls import reverse

from .serializers import KRASerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response  
from django.db import connection


# from django.db.models import Q
from django.shortcuts import render, redirect
from .models import TargetAssignMasterDetails, KraEntryMaster, KraEntryMasterDetails
from datetime import datetime
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery
from urllib.parse import urlencode

import json

from django.db.models import Q, F, Count

from .models import KraEntryMasterDetails
from rest_framework.views import APIView

from django.http import JsonResponse
from django.db.models import F, Value, IntegerField, ExpressionWrapper
from datetime import datetime

import pandas as pd
from rest_framework.decorators import api_view



class KRAViewSet(viewsets.ModelViewSet):
    queryset = KRA.objects.all()
    serializer_class = KRASerializer
    def get_queryset(self):
        return KRA.objects.all().order_by('SortOrder')  # 👈 Order by SortOrder

    @action(detail=True, methods=['post'], url_path='change_sort_order')
    def change_sort_order(self, request, pk=None):
        print("DEBUG - Incoming PUT data:", request.data)  # ✅ Print incoming data
        kra = self.get_object()
        sort_order = request.data.get('sort_order')

        if sort_order is None:
            return Response({'error': 'sort_order not provided'}, status=status.HTTP_400_BAD_REQUEST)

        kra.SortOrder = sort_order
        kra.save()
        return Response({'status': 'Sort order updated'}, status=status.HTTP_200_OK)

def kra_page(request):
    return render(request, 'KRA/kra_page.html')


def KraAdd(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    KID = request.GET.get('KID')
    Kraobj = None
    if KID:
        Kraobj = KRA.objects.filter(id=KID,IsDelete=False).first()
    if request.method == "POST":
          Title = request.POST['Title'] 
          Standard = request.POST['Standard'] 
          Type = request.POST['Type'] 
          if KID:
              Kraobj.Title = Title
              Kraobj.Standard = Standard
              Kraobj.Type = Type
              Kraobj.ModifyBy = UserID
              Kraobj.save()

          else: 
              Kraobj = KRA.objects.create(Title=Title,Standard=Standard,Type=Type,CreatedBy=UserID)
         
          return redirect('KraList')  


    context = {'Kraobj':Kraobj}
    return render(request,"KRA/KraAdd.html",context)
    





class HotelKRAStandardList(APIView):
    def get(self, request, org_id):
        kras = KRA.objects.filter(IsDelete=False)
        standards = HotelKRAStandard.objects.filter(OrganizationID=org_id, IsDelete=False)

        std_map = {s.KRAID: s.StandardValue for s in standards}

        result = []
        for kra in kras:
            result.append({
                'KRAID': kra.id,
                'Title': kra.Title,
                'Source': kra.Source,
                'Select_Value_Type': kra.Select_Value_Type,
                'Defination': kra.Defination,
                'StandardValue': std_map.get(kra.id, "")
            })
        return Response(result)

    def post(self, request):
        data = request.data
        org_id = data.get("OrganizationID")
        updated = []

        for item in data.get("standards", []):
            kra_id = item.get("KRAID")
            val = item.get("StandardValue", "")

            obj, created = HotelKRAStandard.objects.update_or_create(
                OrganizationID=org_id,
                KRAID=kra_id,
                defaults={
                    "StandardValue": val,
                    "ModifyBy": 1,
                    "ModifyDateTime": date.today()
                }
            )
            updated.append(obj.id)
        return Response({"message": "Standards updated", "ids": updated})


def kra_standard_page(request):
    return render(request, "KRA/kra_standard.html")


class HotelKRAStandardList(APIView):
    def get(self, request, org_id):
        kras = KRA.objects.filter(IsDelete=False)
        standards = HotelKRAStandard.objects.filter(OrganizationID=org_id, IsDelete=False)

        # std_map = {s.KRAID: s.StandardValue for s in standards}
        # Map KRAID to a dict of both StandardValue and CompareWithValue
        std_map = {
            s.KRAID: {
                'StandardValue': s.StandardValue,
                'CompareWithValue': s.CompareWithValue,
                'IsApplicable': s.IsApplicable
            }
            for s in standards
        }

        result = []
        for kra in kras:
            standard = std_map.get(kra.id, {})
            result.append({
                'KRAID': kra.id,
                'Title': kra.Title,
                'Source': kra.Source,
                'Select_Value_Type': kra.Select_Value_Type,
                'Defination': kra.Defination,
                # 'StandardValue': std_map.get(kra.id, "")
                'StandardValue': standard.get('StandardValue', ""),
                'CompareWithValue': standard.get('CompareWithValue', ""),
                'IsApplicable': standard.get('IsApplicable', ""),
            })
        return Response(result)

    def post(self, request):
        data = request.data
        org_id = data.get("OrganizationID")
        updated = []

        for item in data.get("standards", []):
            kra_id = item.get("KRAID")
            val = item.get("StandardValue", "")
            compare_val = item.get("CompareWithValue", "")
            IsApplicable_value = item.get("IsApplicableValue", "")
            

            obj, created = HotelKRAStandard.objects.update_or_create(
                OrganizationID=org_id,
                KRAID=kra_id,
                defaults={
                    "StandardValue": val,
                    "CompareWithValue": compare_val,
                    "IsApplicable": IsApplicable_value,
                    "ModifyBy": 1,
                    "ModifyDateTime": date.today()
                }
            )
            updated.append(obj.id)
        return Response({"message": "Standards updated", "ids": updated})




@api_view(['GET'])
def organization_list(request):
    orgs = OrganizationMaster.objects.filter(Activation_status=1,IsDelete=False).all()
    data = [{"OrganizationID": o.OrganizationID, "OrganizationName": o.OrganizationName} for o in orgs]
    return Response(data)



def KraList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Kraobjs = KRA.objects.filter(IsDelete=False)
    context = {'Kraobjs':Kraobjs}
    return render(request,"KRA/KraList.html",context)

import calendar
def TargetAssign(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    SessionEmpCode = request.session["EmployeeCode"]
    SessionDesignation = get_employee_designation_by_EmployeeCode(OrganizationID, SessionEmpCode)
    SessionEmpName = get_employee_names_by_designation(OrganizationID, SessionDesignation)

    current_year = datetime.now().year
    years = [current_year + i for i in range(-3, 2)]

    # Defaults
    selected_year = current_year
    selected_month = datetime.now().month

    # Handle 'year' param safely
    cy = request.GET.get('year', '')
    if cy:
        try:
            parts = cy.split('-')
            if len(parts) == 2:
                selected_month = int(parts[0])
                selected_year = int(parts[1])
            elif len(parts) == 1:  # only year like '2025'
                selected_year = int(parts[0])
                selected_month = 1  # default to January
        except (ValueError, IndexError):
            pass  

    # Handle 'ToYear' param safely
    # ToYear = request.POST.get('ToYear', '')
    # ToYear = request.POST.get('ToYear') or request.GET.get('ToYear')
    ToYear = request.POST.get('SelectedToYear') or request.GET.get('SelectedToYear')
    # print("The ToYear value:: ----------->>", ToYear)

    ToYearselected_year = current_year
    ToYearselected_month = datetime.now().month

    # if ToYear:
    #     try:
    #         parts = ToYear.split('-')
    #         if len(parts) == 2:
    #             ToYearselected_month = int(parts[0])
    #             ToYearselected_year = int(parts[1])
    #         elif len(parts) == 1:  # only year like '2025'
    #             ToYearselected_year = int(parts[0])
    #             ToYearselected_month = 1  # default to January
    #     except (ValueError, IndexError):
    #         pass  # fallback to default values
    
    if ToYear:
        try:
            parts = ToYear.split('-')
            if len(parts) == 2:
                month_part = parts[0].strip()
                year_part = parts[1].strip()

                # Handle month name like "Dec"
                if month_part.isdigit():
                    ToYearselected_month = int(month_part)
                else:
                    ToYearselected_month = list(calendar.month_abbr).index(month_part)

                ToYearselected_year = int(year_part)

        except (ValueError, IndexError):
            pass

    # print(f"Converted ToYear value:: ToYearselected_year: {ToYearselected_year} -- ToYearselected_month:{ToYearselected_month}")

    I = request.GET.get('I', OrganizationID)
    KID = request.GET.get('KID', None)
    
    # print("The KID::", KID)
    selected_employee = request.GET.get('employee')
    orgs = OrganizationList(OrganizationID)
    Emps = TargetAssignNames(request, I, SessionDesignation)
    # Kraobjs = KRA.objects.filter(IsDelete=False)
    
    applicable_kra_ids = HotelKRAStandard.objects.filter(
        OrganizationID=I,
        IsApplicable=True,
        IsDelete=False
    ).values_list('KRAID', flat=True)
    
    Kraobjs = KRA.objects.filter(
        id__in=applicable_kra_ids,
        IsDelete=False
    )

    
    # KID = request.GET.get('KID')
    target_assign = None
    if selected_employee is not None:

        target_assign = TargetAssignMaster.objects.filter(
            IsDelete=False,
            AssignToEmployeeCode=selected_employee,
            OrganizationID=I
        ).filter(
            Q(AssignYear__lt=selected_year) | Q(AssignYear=selected_year, AssignMonth__lte=selected_month),
            Q(AssignToYear__gt=selected_year) | Q(AssignToYear=selected_year, AssignToMonth__gte=selected_month)
        ).first()

            
        target_assign_details = TargetAssignMasterDetails.objects.filter(AssignMaster=target_assign, IsDelete=False, )
        selected_kras = [detail.KRA.id for detail in target_assign_details]  
    else:
        selected_kras = []

    # print("selected_kras = ",selected_kras)

    if request.method == "POST":
        removed_kras = request.POST.get('removed_kras', '[]')
        removed_kras = json.loads(removed_kras)
        # print(removed_kras)
        
        
        AssingToEmployeeCode = request.POST['AssignEmployeeCode']
        AssignOrganizationID = request.POST['AssignOrganizationID']
        # print("AssingToEmployeeCode ----------", AssingToEmployeeCode)
        # print("AssignOrganizationID = ",AssignOrganizationID)
        AssignToDesignation = get_employee_designation_by_EmployeeCode(AssignOrganizationID, AssingToEmployeeCode)
        # AssignToName = get_employee_names_by_designation(AssignOrganizationID, AssignToDesignation)
        AssignToName = get_employee_name_by_code(AssignOrganizationID, AssingToEmployeeCode) or "Unknown"
        AssignYear = request.POST['AssignYear']
        AssignToDOJ = request.POST.get('AssignToDOJ')
        # print("Assign To date of joining::------------", AssignToDOJ)
        # print(f"Assign To date of joining::------------", AssignToDOJ)

        
        selected_kras = request.POST.getlist('selected_kras')

        # Validate no overlapping assignments
        existing_assignments = TargetAssignMaster.objects.filter(
            IsDelete=False,
            AssignToEmployeeCode=AssingToEmployeeCode,
            OrganizationID=AssignOrganizationID
        )

        start_new = selected_year * 12 + selected_month
        end_new = ToYearselected_year * 12 + ToYearselected_month
        # print(f"start_new: {start_new} -- end_new: {end_new}")


        # print(f"AssignYear: {selected_year} -- AssignMonth: {selected_month}")
        # print(f"ToYearselected_year: {ToYearselected_year} -- AssignMonth: {ToYearselected_month}")
        for entry in existing_assignments:
            # ✅ Skip this record if it's the one we're updating
            # if target_assign and str(entry.id) == str(target_assign.id):
            if KID is not None:
                continue

            start_existing = entry.AssignYear * 12 + entry.AssignMonth
            end_existing = entry.AssignToYear * 12 + entry.AssignToMonth

            if not (end_new < start_existing or start_new > end_existing):
                # ✅ You’re in update mode, so preserve KID in the redirect
                redirect_base = f"{request.path}?"
                if KID:
                    redirect_base += f"KID={KID}&"

                error_url = f"{redirect_base}I={AssignOrganizationID}&employee={AssingToEmployeeCode}&year={selected_year}&ToYear={ToYearselected_year}-{ToYearselected_month}&Success=false&message=This range is already assigned. Please delete it first or assign a different range.."
                return redirect(error_url)

        if target_assign is not None:
            # Update existing Target Assignment
            target_assign.AssignByName = SessionEmpName
            target_assign.AssignByEmployeeCode = SessionEmpCode
            target_assign.AssignByDesignation = SessionDesignation
            target_assign.AssignToName = AssignToName
            target_assign.AssignToEmployeeCode = AssingToEmployeeCode
            target_assign.AssignToDesignation = AssignToDesignation
            target_assign.AssignYear = selected_year
            target_assign.AssignMonth = selected_month
            target_assign.AssignToDoj = AssignToDOJ

            
            target_assign.AssignToYear = ToYearselected_year
            target_assign.AssignToMonth = ToYearselected_month
            
            
            target_assign.OrganizationID = AssignOrganizationID
            target_assign.ModifyBy = UserID
            target_assign.save()

            # Delete old KRA assignments before updating with new ones
            for re in removed_kras:
                RD = TargetAssignMasterDetails.objects.filter(
                        AssignMaster=target_assign, 
                        KRA_id=re,IsDelete=False,OrganizationID = AssignOrganizationID
                    ).first()
                
                if RD:
                    RD.IsDelete  =  True
                    RD.ModifyBy = UserID
                    RD.ModifyDateTime = datetime.now()
                    RD.save()

                    # Also soft delete from KraEntryMasterDetails
                    KraEntryMasterDetails.objects.filter(
                        TargetAssignMasterDetails=RD,
                        OrganizationID=AssignOrganizationID,
                        IsDelete=False
                    ).update(
                        IsDelete=True,
                        ModifyBy=UserID,
                        ModifyDateTime=datetime.now()
                    )
        else:
            # Create new Target Assignment
            target_assign = TargetAssignMaster.objects.create(
                AssignByName=SessionEmpName,
                AssignByEmployeeCode=SessionEmpCode,
                AssignByDesignation=SessionDesignation,
                AssignToName=AssignToName,
                AssignToEmployeeCode=AssingToEmployeeCode,
                AssignToDesignation=AssignToDesignation,
                AssignYear = selected_year,
                AssignMonth = selected_month,
                AssignToDoj = AssignToDOJ,
                
                AssignToYear = ToYearselected_year,
                AssignToMonth = ToYearselected_month,
                CreatedByUserName=SessionEmpName,
                AssignDate=datetime.now().date(),
                OrganizationID=AssignOrganizationID,
                # CreatedDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                CreatedDateTime=datetime.now(),
                CreatedBy = UserID
            )
            

        # Assign KRAs
        for kra_id in selected_kras:
            Targetobj = TargetAssignMasterDetails.objects.filter(
                AssignMaster=target_assign,
                KRA_id=kra_id,
                OrganizationID=AssignOrganizationID,
                CreatedBy=UserID,
                IsDelete=False
            ).first()
            if Targetobj is  None:
                TargetAssignMasterDetails.objects.create(
                    AssignMaster=target_assign,
                    KRA_id=kra_id,
                    OrganizationID=AssignOrganizationID,
                    CreatedBy=UserID,
                )

        url = reverse('TargetAssignList')
        redirect_url = f"{url}?I={AssignOrganizationID}&year={AssignYear}"
        return redirect(redirect_url)
        
    context = {
        'Kraobjs': Kraobjs,
        'orgs': orgs,
        'Emps': Emps,
        'years': years,
        'selected_year': selected_year,
        'selected_employee': selected_employee,
        'I': I,
        'selected_kras': selected_kras,
        'target_assign': target_assign if selected_employee else None,
        'selected_to_year': ToYearselected_year,
        'selected_to_month': ToYearselected_month,
        'error_message': request.GET.get('message') if request.GET.get('Success', '').lower() == 'false' else None,
    }
    return render(request, "KRA/TargetAssign.html", context)


# def Bulk_TargetAssign(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     SessionEmpCode = request.session["EmployeeCode"]
#     SessionDesignation = get_employee_designation_by_EmployeeCode(OrganizationID, SessionEmpCode)
#     SessionEmpName = get_employee_names_by_designation(OrganizationID, SessionDesignation)

#     current_year = datetime.now().year
#     years = [current_year + i for i in range(-3, 2)]

#     # Defaults
#     selected_year = current_year
#     selected_month = datetime.now().month

#     # Handle 'year' param safely
#     cy = request.GET.get('year', '')
#     if cy:
#         try:
#             parts = cy.split('-')
#             if len(parts) == 2:
#                 selected_month = int(parts[0])
#                 selected_year = int(parts[1])
#             elif len(parts) == 1:  # only year like '2025'
#                 selected_year = int(parts[0])
#                 selected_month = 1  # default to January
#         except (ValueError, IndexError):
#             pass  # fallback to default year/month

#     # Handle 'ToYear' param safely
#     # ToYear = request.POST.get('ToYear', '')
#     # ToYear = request.POST.get('ToYear') or request.GET.get('ToYear')
#     ToYear = request.POST.get('SelectedToYear') or request.GET.get('SelectedToYear')
#     # print("The ToYear value:: ----------->>", ToYear)

#     ToYearselected_year = current_year
#     ToYearselected_month = datetime.now().month

#     if ToYear:
#         try:
#             parts = ToYear.split('-')
#             if len(parts) == 2:
#                 ToYearselected_month = int(parts[0])
#                 ToYearselected_year = int(parts[1])
#             elif len(parts) == 1:  # only year like '2025'
#                 ToYearselected_year = int(parts[0])
#                 ToYearselected_month = 1  # default to January
#         except (ValueError, IndexError):
#             pass  # fallback to default values

#     # print("Converted ToYear value (ToYearselected_year)-(ToYearselected_month):: ----------->>", ToYearselected_year, '--' ,ToYearselected_month)

#     I = request.GET.get('I', OrganizationID)
#     KID = request.GET.get('KID', None)
#     # print("The KID::", KID)
#     selected_employee = request.GET.get('employee')
#     orgs = OrganizationList(OrganizationID)
#     Emps = TargetAssignNames(request, I, SessionDesignation)
#     # Kraobjs = KRA.objects.filter(IsDelete=False)
    
#     applicable_kra_ids = HotelKRAStandard.objects.filter(
#         OrganizationID=I,
#         IsApplicable=True,
#         IsDelete=False
#     ).values_list('KRAID', flat=True)
    
#     Kraobjs = KRA.objects.filter(
#         id__in=applicable_kra_ids,
#         IsDelete=False
#     )

    
#     # KID = request.GET.get('KID')
#     target_assign = None
#     if selected_employee is not None:

#         target_assign = TargetAssignMaster.objects.filter(
#             IsDelete=False,
#             AssignToEmployeeCode=selected_employee,
#             OrganizationID=I
#         ).filter(
#             Q(AssignYear__lt=selected_year) | Q(AssignYear=selected_year, AssignMonth__lte=selected_month),
#             Q(AssignToYear__gt=selected_year) | Q(AssignToYear=selected_year, AssignToMonth__gte=selected_month)
#         ).first()

            
#         target_assign_details = TargetAssignMasterDetails.objects.filter(AssignMaster=target_assign, IsDelete=False, )
#         selected_kras = [detail.KRA.id for detail in target_assign_details]  
#     else:
#         selected_kras = []

#     # print("selected_kras = ",selected_kras)

#     if request.method == "POST":
#         removed_kras = request.POST.get('removed_kras', '[]')
#         removed_kras = json.loads(removed_kras)
#         # print(removed_kras)
        
        
#         AssingToEmployeeCode = request.POST['AssignEmployeeCode']
#         AssignOrganizationID = request.POST['AssignOrganizationID']
#         # print("AssingToEmployeeCode ----------", AssingToEmployeeCode)
#         # print("AssignOrganizationID = ",AssignOrganizationID)
#         AssignToDesignation = get_employee_designation_by_EmployeeCode(AssignOrganizationID, AssingToEmployeeCode)
#         # AssignToName = get_employee_names_by_designation(AssignOrganizationID, AssignToDesignation)
#         AssignToName = get_employee_name_by_code(AssignOrganizationID, AssingToEmployeeCode) or "Unknown"
#         AssignYear = request.POST['AssignYear']
#         AssignToDOJ = request.POST.get('AssignToDOJ')
#         # print("Assign To date of joining::------------", AssignToDOJ)

        
#         selected_kras = request.POST.getlist('selected_kras')

#         # Validate no overlapping assignments
#         existing_assignments = TargetAssignMaster.objects.filter(
#             IsDelete=False,
#             AssignToEmployeeCode=AssingToEmployeeCode,
#             OrganizationID=AssignOrganizationID
#         )

#         start_new = selected_year * 12 + selected_month
#         end_new = ToYearselected_year * 12 + ToYearselected_month

#         for entry in existing_assignments:
#             # ✅ Skip this record if it's the one we're updating
#             # if target_assign and str(entry.id) == str(target_assign.id):
#             if KID is not None:
#                 continue

#             start_existing = entry.AssignYear * 12 + entry.AssignMonth
#             end_existing = entry.AssignToYear * 12 + entry.AssignToMonth

#             if not (end_new < start_existing or start_new > end_existing):
#                 # ✅ You’re in update mode, so preserve KID in the redirect
#                 redirect_base = f"{request.path}?"
#                 if KID:
#                     redirect_base += f"KID={KID}&"

#                 error_url = f"{redirect_base}I={AssignOrganizationID}&employee={AssingToEmployeeCode}&year={selected_year}&ToYear={ToYearselected_year}-{ToYearselected_month}&Success=false&message=This range is already assigned. Please delete it first or assign a different range.."
#                 return redirect(error_url)



#         if target_assign is not None:
#             # Update existing Target Assignment
#             target_assign.AssignByName = SessionEmpName
#             target_assign.AssignByEmployeeCode = SessionEmpCode
#             target_assign.AssignByDesignation = SessionDesignation
#             target_assign.AssignToName = AssignToName
#             target_assign.AssignToEmployeeCode = AssingToEmployeeCode
#             target_assign.AssignToDesignation = AssignToDesignation
#             target_assign.AssignYear = selected_year
#             target_assign.AssignMonth = selected_month
#             target_assign.AssignToDoj = AssignToDOJ

            
#             target_assign.AssignToYear = ToYearselected_year
#             target_assign.AssignToMonth = ToYearselected_month
            
            
#             target_assign.OrganizationID = AssignOrganizationID
#             target_assign.ModifyBy = UserID
#             target_assign.save()

#             # Delete old KRA assignments before updating with new ones
#             for re in removed_kras:
#                 RD = TargetAssignMasterDetails.objects.filter(
#                         AssignMaster=target_assign, 
#                         KRA_id=re,IsDelete=False,OrganizationID = AssignOrganizationID
#                     ).first()
                
#                 if RD:
#                     RD.IsDelete  =  True
#                     RD.ModifyBy = UserID
#                     RD.ModifyDateTime = datetime.now()
#                     RD.save()

#                     # Also soft delete from KraEntryMasterDetails
#                     KraEntryMasterDetails.objects.filter(
#                         TargetAssignMasterDetails=RD,
#                         OrganizationID=AssignOrganizationID,
#                         IsDelete=False
#                     ).update(
#                         IsDelete=True,
#                         ModifyBy=UserID,
#                         ModifyDateTime=datetime.now()
#                     )
#         else:
#             # Create new Target Assignment
#             target_assign = TargetAssignMaster.objects.create(
#                 AssignByName=SessionEmpName,
#                 AssignByEmployeeCode=SessionEmpCode,
#                 AssignByDesignation=SessionDesignation,
#                 AssignToName=AssignToName,
#                 AssignToEmployeeCode=AssingToEmployeeCode,
#                 AssignToDesignation=AssignToDesignation,
#                 AssignYear = selected_year,
#                 AssignMonth = selected_month,
#                 AssignToDoj = AssignToDOJ,
                
#                 AssignToYear = ToYearselected_year,
#                 AssignToMonth = ToYearselected_month,
#                 CreatedByUserName=SessionEmpName,
#                 AssignDate=datetime.now().date(),
#                 OrganizationID=AssignOrganizationID,
#                 # CreatedDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 CreatedDateTime=datetime.now(),
#                 CreatedBy = UserID
#             )
            

#         # Assign KRAs
#         for kra_id in selected_kras:
#             Targetobj = TargetAssignMasterDetails.objects.filter(
#                 AssignMaster=target_assign,
#                 KRA_id=kra_id,
#                 OrganizationID=AssignOrganizationID,
#                 CreatedBy=UserID,
#                 IsDelete=False
#             ).first()
#             if Targetobj is  None:
#                 TargetAssignMasterDetails.objects.create(
#                     AssignMaster=target_assign,
#                     KRA_id=kra_id,
#                     OrganizationID=AssignOrganizationID,
#                     CreatedBy=UserID,
#                 )

#         url = reverse('TargetAssignList')
#         redirect_url = f"{url}?I={AssignOrganizationID}&year={AssignYear}"
#         return redirect(redirect_url)
        
#     context = {
#         'Kraobjs': Kraobjs,
#         'orgs': orgs,
#         'Emps': Emps,
#         'years': years,
#         'selected_year': selected_year,
#         'selected_employee': selected_employee,
#         'I': I,

#         'selected_kras': selected_kras,
#         'target_assign': target_assign if selected_employee else None,

#         'selected_to_year': ToYearselected_year,
#         'selected_to_month': ToYearselected_month,

#         'error_message': request.GET.get('message') if request.GET.get('Success', '').lower() == 'false' else None,

#     }
#     return render(request, "KRA/Bulk_TargetAssign.html", context)



from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from datetime import datetime
import json


# def Bulk_TargetAssign(request):
#     # 🔐 Session check
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

#     SessionOrgID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     SessionEmpCode = request.session["EmployeeCode"]
#     SessionDesignation = get_employee_designation_by_EmployeeCode(SessionOrgID, SessionEmpCode)
#     SessionEmpName = get_employee_names_by_designation(SessionOrgID, SessionDesignation)

#     # 📅 Year setup
#     current_year = datetime.now().year
#     current_month = datetime.now().month
#     years = [current_year + i for i in range(-3, 2)]

#     selected_year = current_year
#     selected_month = current_month

#     cy = request.GET.get('year')
#     if cy:
#         try:
#             m, y = cy.split('-')
#             selected_month = int(m)
#             selected_year = int(y)
#         except:
#             pass

#     ToYearselected_year = current_year
#     ToYearselected_month = current_month

#     ToYear = request.GET.get('SelectedToYear') or request.POST.get('SelectedToYear')
#     if ToYear:
#         try:
#             m, y = ToYear.split('-')
#             ToYearselected_month = int(m)
#             ToYearselected_year = int(y)
#         except:
#             pass

#     # 🔎 Filters
#     I = request.GET.get('I')  # Organization
#     selected_employee = request.GET.get('employee')
#     KID = request.GET.get('KID')

#     # 🏢 Organizations & Employees (for dropdowns)
#     orgs = OrganizationList(SessionOrgID)
#     Emps = TargetAssignNames(request, I or SessionOrgID, SessionDesignation)

#     # 📌 Applicable KRAs (org-wise)
#     kra_org_id = I or SessionOrgID
#     applicable_kra_ids = HotelKRAStandard.objects.filter(
#         OrganizationID=kra_org_id,
#         IsApplicable=True,
#         IsDelete=False
#     ).values_list('KRAID', flat=True)

#     Kraobjs = KRA.objects.filter(
#         id__in=applicable_kra_ids,
#         IsDelete=False
#     )

#     # ===========================
#     # ✅ DEFAULT DATA (IMPORTANT)
#     # ===========================
#     assignments = TargetAssignMaster.objects.filter(IsDelete=False)

#     if I:
#         assignments = assignments.filter(OrganizationID=I)

#     if selected_employee:
#         assignments = assignments.filter(AssignToEmployeeCode=selected_employee)

#     assignments = assignments.filter(
#         Q(AssignYear__lt=selected_year) | Q(AssignYear=selected_year, AssignMonth__lte=selected_month),
#         Q(AssignToYear__gt=selected_year) | Q(AssignToYear=selected_year, AssignToMonth__gte=selected_month)
#     )

#     # ===========================
#     # Selected assignment (edit mode)
#     # ===========================
#     target_assign = None
#     selected_kras = []

#     if selected_employee:
#         target_assign = assignments.first()

#         if target_assign:
#             details = TargetAssignMasterDetails.objects.filter(
#                 AssignMaster=target_assign,
#                 IsDelete=False
#             )
#             selected_kras = [d.KRA.id for d in details]

#     # ===========================
#     # POST (CREATE / UPDATE)
#     # ===========================
#     if request.method == "POST":
#         removed_kras = json.loads(request.POST.get('removed_kras', '[]'))

#         AssignEmployeeCode = request.POST['AssignEmployeeCode']
#         AssignOrganizationID = request.POST['AssignOrganizationID']
#         AssignToDesignation = get_employee_designation_by_EmployeeCode(
#             AssignOrganizationID, AssignEmployeeCode
#         )
#         AssignToName = get_employee_name_by_code(
#             AssignOrganizationID, AssignEmployeeCode
#         ) or "Unknown"

#         AssignToDOJ = request.POST.get('AssignToDOJ')
#         selected_kras = request.POST.getlist('selected_kras')

#         # Overlap check
#         existing = TargetAssignMaster.objects.filter(
#             IsDelete=False,
#             AssignToEmployeeCode=AssignEmployeeCode,
#             OrganizationID=AssignOrganizationID
#         )

#         start_new = selected_year * 12 + selected_month
#         end_new = ToYearselected_year * 12 + ToYearselected_month

#         for e in existing:
#             if KID:
#                 continue

#             start_old = e.AssignYear * 12 + e.AssignMonth
#             end_old = e.AssignToYear * 12 + e.AssignToMonth

#             if not (end_new < start_old or start_new > end_old):
#                 return redirect(
#                     f"{request.path}?Success=false&message=Date range already assigned"
#                 )

#         if target_assign:
#             target_assign.AssignToName = AssignToName
#             target_assign.AssignToEmployeeCode = AssignEmployeeCode
#             target_assign.AssignToDesignation = AssignToDesignation
#             target_assign.AssignYear = selected_year
#             target_assign.AssignMonth = selected_month
#             target_assign.AssignToYear = ToYearselected_year
#             target_assign.AssignToMonth = ToYearselected_month
#             target_assign.AssignToDoj = AssignToDOJ
#             target_assign.ModifyBy = UserID
#             target_assign.save()
#         else:
#             target_assign = TargetAssignMaster.objects.create(
#                 AssignByName=SessionEmpName,
#                 AssignByEmployeeCode=SessionEmpCode,
#                 AssignByDesignation=SessionDesignation,
#                 AssignToName=AssignToName,
#                 AssignToEmployeeCode=AssignEmployeeCode,
#                 AssignToDesignation=AssignToDesignation,
#                 AssignYear=selected_year,
#                 AssignMonth=selected_month,
#                 AssignToYear=ToYearselected_year,
#                 AssignToMonth=ToYearselected_month,
#                 AssignToDoj=AssignToDOJ,
#                 OrganizationID=AssignOrganizationID,
#                 CreatedBy=UserID,
#                 CreatedDateTime=datetime.now()
#             )

#         # Remove KRAs
#         TargetAssignMasterDetails.objects.filter(
#             AssignMaster=target_assign,
#             KRA_id__in=removed_kras,
#             IsDelete=False
#         ).update(IsDelete=True, ModifyBy=UserID, ModifyDateTime=datetime.now())

#         # Add KRAs
#         for kid in selected_kras:
#             TargetAssignMasterDetails.objects.get_or_create(
#                 AssignMaster=target_assign,
#                 KRA_id=kid,
#                 OrganizationID=AssignOrganizationID,
#                 defaults={'CreatedBy': UserID}
#             )

#         return redirect(reverse('TargetAssignList'))

#     # ===========================
#     # CONTEXT
#     # ===========================
#     context = {
#         'Kraobjs': Kraobjs,
#         'orgs': orgs,
#         'Emps': Emps,
#         'years': years,
#         'assignments': assignments,   # 🔥 MAIN TABLE DATA
#         'selected_employee': selected_employee,
#         'selected_kras': selected_kras,
#         'target_assign': target_assign,
#         'selected_year': selected_year,
#         'selected_to_year': ToYearselected_year,
#         'selected_to_month': ToYearselected_month,
#         'I': I,
#         'error_message': request.GET.get('message')
#     }

#     return render(request, "KRA/Bulk_TargetAssign.html", context)



def TargetAssignList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
   
    SessionEmpCode = request.session["EmployeeCode"]
    SessionDesignation = get_employee_designation_by_EmployeeCode(OrganizationID, SessionEmpCode)
 
    
    current_year = datetime.now().year
    years = [current_year + i for i in range(-3, 2)]
    rr =request.GET.get('year','')
    # if rr:
    #     rr = rr.split('-')
    #     if len(rr) == 2:
    #         selected_month = int(rr[0])
    #         selected_year = int(rr[1])
    #     else:
    #         selected_year = current_year
    #         selected_month= datetime.now().month
    # else:
    #     selected_year = current_year
    #     selected_month = datetime.now().month

    if rr:
        try:
            parts = rr.split('-')
            if len(parts) == 2:
                selected_month = int(parts[0])
                selected_year = int(parts[1])
            elif len(parts) == 1:  # only year like '2025'
                selected_year = int(parts[0])
                selected_month = 1  # default to January
        except (ValueError, IndexError):
            pass  # fallback to default year/month
    else:
        selected_year = current_year
        selected_month = datetime.now().month
    
    
    I = request.GET.get('I', OrganizationID)
    
    orgs = OrganizationList(OrganizationID)
    
    TargetList = TargetAssignMaster.objects.filter(IsDelete=False,OrganizationID=I,AssignByDesignation=SessionDesignation,AssignYear=selected_year)
    

    print("Selected year is here::", selected_year)
   
        
    context = {
        'orgs': orgs,
        'years': years,
        'selected_year': selected_year,
        'I': I,
        'TargetList':TargetList
    }
    return render(request, "KRA/TargetAssignList.html", context)



def Delete_Targeted_Assign(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    SessionEmpCode = request.session["EmployeeCode"]

    UserOrganizationID = request.GET.get('I', OrganizationID)
    KID = request.GET.get('KID', None)
    selected_employee = request.GET.get('employee')
    year = request.GET.get('year')
    # selected_year = request.GET.get('selected_year')
    print("My Year value is here::", year)

    if year:
        try:
            parts = year.split('-')
            if len(parts) == 2:
                selected_month = int(parts[0])
                selected_year = int(parts[1])
            elif len(parts) == 1:  # only year like '2025'
                selected_year = int(parts[0])
                selected_month = 1  # default to January
        except (ValueError, IndexError):
            pass  # fallback to default year/month

    print("My Year value is here::", selected_year)

    if KID and selected_employee:
        existing_assignments = TargetAssignMaster.objects.filter(
            IsDelete=False,
            AssignToEmployeeCode=selected_employee,
            OrganizationID=UserOrganizationID,
            id = KID
        ).first()

        if existing_assignments:
            existing_assignments.IsDelete = True
            existing_assignments.ModifyBy = UserID
            existing_assignments.ModifyDateTime = datetime.now()
            existing_assignments.save()
        else:
            print("The assignments object is not found")
    else:
        print("The KID and selected employee code is not found")
    
    url = reverse('TargetAssignList')
    redirect_url = f"{url}?I={UserOrganizationID}&year={selected_year}"
    return redirect(redirect_url)





def KraEnrty(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    SessionEmpCode = request.session["EmployeeCode"]
    
    SessionDesignation = get_employee_designation_by_EmployeeCode(OrganizationID, SessionEmpCode)
    # selected_employee = request.GET.get('employee', SessionEmpCode).zfill(7)
    # if UserID=="20201212180048":
    #     OrganizationID=501
    #     SessionEmpCode="77"
    I = request.GET.get('I', OrganizationID)
    selected_employee = request.GET.get('employee', SessionEmpCode)

    Emps = TargetAssignNamesWithReportingtoDesignationEmployeeNameCode(request, I, SessionDesignation)
    
    SubmittedByDesignation =  get_employee_name_designation_by_EmployeeCode(I, selected_employee)
    Employee = get_employee_name_designation_by_EmployeeCode(I, selected_employee)
    # orgs = OrganizationName(OrganizationID)
    orgs = OrganizationList(OrganizationID)
    current_year = datetime.now().year
    current_month = datetime.now().strftime('%m')
    
    years = [current_year + 1, current_year, current_year - 1, current_year - 2, current_year - 3]
    
    selected_year = request.GET.get('year', current_year)
    selected_month = request.GET.get('month', int(current_month))

    # Convert to int safely
    try:
        selected_year = int(selected_year)
    except (TypeError, ValueError):
        selected_year = current_year

    try:
        selected_month = int(selected_month)
    except (TypeError, ValueError):
        selected_month = datetime.now().month

  
    standard_subquery = HotelKRAStandard.objects.filter(
        KRAID=OuterRef('KRA__id'),
        OrganizationID=I,
        IsDelete=False
    ).values('StandardValue')[:1]

    Kraobjs = TargetAssignMasterDetails.objects.filter(
        Q(AssignMaster__AssignYear=selected_year) | Q(AssignMaster__AssignToYear=selected_year),
        OrganizationID=I,
        AssignMaster__AssignToEmployeeCode=selected_employee,
        IsDelete=False
    ).annotate(
        StandardValue=Subquery(standard_subquery)
    )

    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC KRA_Entry_Select_Revised @OrganizationID=%s, @EntryYear=%s, @EntryMonth=%s, @UserID=%s, @UID=%s, @EmpCode=%s",
            [I, selected_year, selected_month, UserID, UserID, selected_employee]
        )   

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    

    # ✅ Insert deduplication logic here:
    unique_rows = {}
    for row in rowslist:
        kra_id = row.get("id")  # Change key name if your field is different
        if kra_id not in unique_rows:
            unique_rows[kra_id] = row

    # Final deduplicated list:
    rowslist = list(unique_rows.values())
    
    KraEntryobj  = KraEntryMaster.objects.filter(
        OrganizationID=I,
        IsDelete=False,
        SubmittedByEmployeeCode=selected_employee,
        SubmittedYear=selected_year,
        SubmittedMonth=selected_month
    ).first()
   
    if KraEntryobj:
        KraEntryDetailsobj  = KraEntryMasterDetails.objects.filter(OrganizationID=I,IsDelete=False,KraEntryMaster=KraEntryobj)
        KraDetailsMap = {detail.TargetAssignMasterDetails.KRA.id: {'Actual': detail.Actual, 'ActualValue': detail.ActualValue} for detail in KraEntryDetailsobj}
        for kra in Kraobjs:
            detail_data = KraDetailsMap.get(kra.KRA.id)
            if detail_data:
                kra.Actual = detail_data['Actual']
                kra.ActualValue = detail_data['ActualValue']
    else:
         for kra in Kraobjs:
            kra.Actual =  ''
            
            kra.save()
   

    if request.method == "POST":
        selected_year = request.POST.get('year')
        selected_month = request.POST.get('month')
        
        IsSave = 'SaveEntry' in request.POST
        IsFinalSubmit = 'FinalSubmit' in request.POST

        # print("IsSave:", IsSave)
        # print("IsFinalSubmit:", IsFinalSubmit)

        if IsSave:
            # print("Save Entry clicked")
            SubmitMode = 'Save'
        elif IsFinalSubmit:
            SubmitMode = 'Final Submit'
        else:        
            SubmitMode = 'Unknown'

        KraEntryobj  = KraEntryMaster.objects.filter(
            OrganizationID=I,
            IsDelete=False,
            SubmittedByEmployeeCode=selected_employee,
            SubmittedYear=selected_year,
            SubmittedMonth=selected_month
        ).first()
        
        if not KraEntryobj:
            KraEntryobj = KraEntryMaster.objects.create(
                SubmittedByEmployeeCode=selected_employee,
                SubmittedByName=Employee,
                SubmittedByDesignation = SubmittedByDesignation,
                SubmittedYear=selected_year,
                SubmittedMonth=selected_month,
                OrganizationID=I,
                CreatedBy=UserID,
                ModifyBy=UserID,
                IsSave=IsSave,
                IsFinalSubmit=IsFinalSubmit,
            )

            # if IsSave:
            #     KraEntryobj.IsSave = True
        # print("KRA Count:", Kraobjs.count())
        for Kr in Kraobjs:
            actual_value = request.POST.get(f'actual_{Kr.KRA.id}', None)
            actual_Datavalue = request.POST.get(f'ActualValue_{Kr.KRA.id}', None)
            Standard__Datavalue = request.POST.get(f'Standard_{Kr.KRA.id}', None)
            # kra_id_str = request.POST.get(f'KRAID_{Kr.id}', '')
            
            if actual_value is not None:
                existing_record = KraEntryMasterDetails.objects.filter(
                    KraEntryMaster=KraEntryobj,
                    TargetAssignMasterDetails=Kr, IsDelete=False
                ).first()

                if existing_record:
                    # print("The Issave saved values::", existing_record.KraEntryMaster.IsSave)
                    # print("The IsSubmit  values::", existing_record.KraEntryMaster.IsSave)
                    existing_record.Actual = actual_value
                    existing_record.ActualValue = actual_Datavalue
                    existing_record.StandardValue = Standard__Datavalue
                    existing_record.ModifyBy = UserID
                    existing_record.ModifyDateTime = datetime.now().date()

                    if not existing_record.KraEntryMaster.IsSave and IsSave:
                        print("The saved value is False in database")
                        existing_record.KraEntryMaster.IsSave = True

                    if not existing_record.KraEntryMaster.IsFinalSubmit and IsFinalSubmit:
                        print("The Final Submit value is False in database")
                        existing_record.KraEntryMaster.IsFinalSubmit = True

                    existing_record.KraEntryMaster.ModifyBy = UserID
                    existing_record.KraEntryMaster.ModifyDateTime = datetime.now().date()
                    existing_record.KraEntryMaster.save()  # ✅ Save changes to KraEntryMaster

                    existing_record.save()
                else:
                    KraEntryMasterDetails.objects.create(
                        KraEntryMaster=KraEntryobj,
                        TargetAssignMasterDetails=Kr,
                        Actual=actual_value,
                        ActualValue = actual_Datavalue,
                        StandardValue = Standard__Datavalue,
                        OrganizationID=I,
                        KRAID=Kr.KRA.id,
                        CreatedBy=UserID,
                        # KraEntryMaster
                    )

                    # Update save/submit flags on parent (if not already True)
                    updated = False
                    if not KraEntryobj.IsSave and IsSave:
                        KraEntryobj.IsSave = True
                        updated = True

                    if not KraEntryobj.IsFinalSubmit and IsFinalSubmit:
                        KraEntryobj.IsFinalSubmit = True
                        updated = True

                    if updated:
                        KraEntryobj.ModifyBy = UserID
                        KraEntryobj.ModifyDateTime = datetime.now().date()
                        KraEntryobj.save()
                    
        # url = reverse('KraEnrty')
        # redirect_url = f"{url}?year={selected_year}&month={selected_month}&I={I}&employee={selected_employee}"
        # return redirect(redirect_url)

        # Determine redirect parameters after processing all entries
        KraEntryDetailsobj = None
        action = 'edit' if KraEntryobj and KraEntryDetailsobj else 'submit'
        params = {
            'I': I,
            'year': selected_year,
            'month': selected_month,
            'employee': selected_employee,
            'Success': 'True',
            'action': action,
            'message': f'KRA Entry {"Updated" if action == "edit" else "Created"} Successfully via {SubmitMode}!'
        }
        url = f"{reverse('KraEnrty')}?{urlencode(params)}"
        return redirect(url)

    context = {
        'rowslist': rowslist,
        'I': int(I),
        'selected_employee':selected_employee,
        'Kraobjs': rowslist,
        'Emps':Emps,
        'Employee': Employee,
        'years': years,
        'current_month': current_month,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'orgs':orgs
    }

    return render(request, "KRA/KraEnrty.html", context)



# ------------------------------------ Experiments --------------------------------
def KraYearlyReport(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = request.session["UserID"]
    SessionEmpCode = request.session["EmployeeCode"]

    # if UserID=="20201212180048":
    #     OrganizationID=501
    #     SessionEmpCode="77"

    SessionDesignation = get_employee_designation_by_EmployeeCode(OrganizationID, SessionEmpCode)
   
    UserOrganizationID = request.GET.get('I', OrganizationID)
    # I = request.GET.get('I', OrganizationID)
    selected_employee = request.GET.get('employee', SessionEmpCode)
    # AssignYear = request.GET.get('AssignYear')
    from_year = request.GET.get('FromYear')
    to_year = request.GET.get('ToYear')

    Emps = TargetAssignNamesWithReportingtoDesignationEmployeeNameCode(request, UserOrganizationID, SessionDesignation)
    # Emps = TargetAssignNamesWithReportingtoDesignationEmployeeNameCode_New(request, UserOrganizationID, SessionDesignation)
    # Emps = TargetAssignNamesWithReportingtoDesignationEmployeeNameCode(request, I, SessionDesignation)
    orgs = OrganizationList(OrganizationID)
    
    current_year = datetime.now().year
    # current_year = datetime.now().year
    years = [current_year + i for i in range(-3, 2)]

    # years = [current_year + 1, current_year, current_year - 1, current_year - 2, current_year - 3]
    selected_year = int(request.GET.get('year', current_year))
   
    context = {
        'orgs': orgs,
        'Emps':Emps,
        'I': UserOrganizationID,
        'selected_year': selected_year,
        'from_year': from_year,
        'to_year': to_year,
        'years': years,
        'selected_employee':selected_employee
    }

    return render(request, "KRA/KraYearlyReport.html", context)



# ------------------------------------------- Testing -- Experimental Code ------------------------------


# helper function at the top
def generate_month_range(from_month, from_year, to_month, to_year):
    result = []
    current = datetime(from_year, from_month, 1)
    end = datetime(to_year, to_month, 1)
    while current <= end:
        result.append(current.strftime('%b-%Y'))  # e.g., "May-2024"
        if current.month == 12:
            current = datetime(current.year + 1, 1, 1)
        else:
            current = datetime(current.year, current.month + 1, 1)
    return result



#  ------------------- Trial --------
def get_kra_yearly_report_json(request, organization_id, employee_code, from_year_str, to_year_str):
    if not from_year_str or not to_year_str:
        return JsonResponse({"error": "Missing FromYear or ToYear"}, status=400)
    
    if organization_id:
        organization_id = int(organization_id)
    print(from_year_str)
    # Convert to comparable integers
    from_month, from_year = map(int, from_year_str.split('-'))
    to_month, to_year = map(int, to_year_str.split('-'))

    from_key = from_year * 100 + from_month
    to_key = to_year * 100 + to_month

    # print("from_year number:: ", from_year)
    # print("to_year number:: ", to_year)

    # Annotate comparable key
    qs = KraEntryMasterDetails.objects.filter(
        KraEntryMaster__OrganizationID=organization_id,
        KraEntryMaster__SubmittedByEmployeeCode=employee_code,
        KraEntryMaster__IsDelete=False,
        IsDelete=False,
        TargetAssignMasterDetails__IsDelete=False,
        TargetAssignMasterDetails__AssignMaster__IsDelete=False,  
    ).annotate(
        EntryKey=ExpressionWrapper(
            F('KraEntryMaster__SubmittedYear') * 100 + F('KraEntryMaster__SubmittedMonth'),
            output_field=IntegerField()
        )
    ).filter(
        EntryKey__gte=from_key,
        EntryKey__lte=to_key,
    ).select_related(
        'KraEntryMaster', 'TargetAssignMasterDetails__KRA'
    ).annotate(
        Title=F('TargetAssignMasterDetails__KRA__Title'),
        SortOrder=F('TargetAssignMasterDetails__KRA__SortOrder'),
        # Standard=F('TargetAssignMasterDetails__KRA__Standard'),
        Standard=F('StandardValue'),
        Month=F('KraEntryMaster__SubmittedMonth'),
        Rating=F('Actual'),
        # Rating=F('PerformanceRating'),
    ).order_by('SortOrder').values('Title', 'Standard', 'Month', 'Rating', 'ActualValue', 'KraEntryMaster__SubmittedYear','SortOrder')


    df = pd.DataFrame(list(qs))

    if df.empty:
        return JsonResponse([], safe=False)

    df['Standard'] = df['Standard'].astype(str)
    df['Title'] = df['Title'].astype(str)
    df['Month'] = df['Month'].astype(int)

    month_map = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    df['Year'] = df['KraEntryMaster__SubmittedYear'].astype(int)
    df['MonthYear'] = df.apply(lambda row: f"{month_map[row['Month']]}-{row['Year']}", axis=1)


    standard_lookup = df.groupby("Title")['Standard'].first()

    # Create pivot tables
    pivot_rating = df.pivot_table(index='Title', columns='MonthYear', values='Rating', aggfunc='first').fillna('')
    pivot_actual = df.pivot_table(index='Title', columns='MonthYear', values='ActualValue', aggfunc='first').fillna('')
    pivot_standard = df.pivot_table(index='Title', columns='MonthYear', values='Standard', aggfunc='first').fillna('')


    full_month_range = generate_month_range(from_month, from_year, to_month, to_year)

    for col in full_month_range:
        if col not in df['MonthYear'].values:
            for field in ['', '_Actual', '_Standard']:
                pivot_rating[col] = pivot_rating.get(col, '')
                pivot_actual[f"{col}_Actual"] = pivot_actual.get(f"{col}_Actual", '')
                pivot_standard[f"{col}_Standard"] = pivot_standard.get(f"{col}_Standard", '')



    pivot_actual.columns = [f"{col}_Actual" for col in pivot_actual.columns]
    pivot_standard.columns = [f"{col}_Standard" for col in pivot_standard.columns]

    final_df = pivot_rating.join([pivot_actual, pivot_standard], how='outer').reset_index()
    title_sort_map = df[['Title', 'SortOrder']].drop_duplicates().set_index('Title')['SortOrder']
    final_df['SortOrder'] = final_df['Title'].map(title_sort_map)


    def get_overall_rating(row):
        priority = {
            'Exceeds Expectation': 1,
            'Met': 2,
            'Not Met': 3,
            'N/A': 99  
        }

        rating_cols = [col for col in row.index if '-' in col and not col.endswith('_Actual') and not col.endswith('_Standard')]
        values = row[rating_cols]
        valid_ratings = values[values != '']

        if valid_ratings.empty:
            return ''

        filtered = valid_ratings[valid_ratings != 'N/A']

        if not filtered.empty:
            counts = filtered.value_counts()
        else:
            counts = valid_ratings.value_counts()

        max_count = counts.max()
        top_ratings = [rating for rating, count in counts.items() if count == max_count]

        top_ratings.sort(key=lambda x: priority.get(x, 99))
        return top_ratings[0]
    
    final_df['OverallRating'] = final_df.apply(get_overall_rating, axis=1)
    final_df.sort_values('SortOrder', inplace=True)
    final_df.drop(columns='SortOrder', inplace=True)
    result = final_df.reset_index().to_dict(orient='records')
    return JsonResponse(result, safe=False)













# -------------------------------------------- Previous Code ----------------------------------

def KraYearlyReportPrevious(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = request.session["UserID"]
    SessionEmpCode = request.session["EmployeeCode"]

    # if UserID=="20201212180048":
    #     OrganizationID=501
    #     SessionEmpCode="77"

    SessionDesignation = get_employee_designation_by_EmployeeCode(OrganizationID, SessionEmpCode)
   
    UserOrganizationID = request.GET.get('I', OrganizationID)
    # I = request.GET.get('I', OrganizationID)
    selected_employee = request.GET.get('employee', SessionEmpCode)
    # AssignYear = request.GET.get('AssignYear')
    # from_year = request.GET.get('FromYear')
    # to_year = request.GET.get('ToYear')

    Emps = TargetAssignNamesWithReportingtoDesignationEmployeeNameCode(request, UserOrganizationID, SessionDesignation)
    # Emps = TargetAssignNamesWithReportingtoDesignationEmployeeNameCode_New(request, UserOrganizationID, SessionDesignation)
    # Emps = TargetAssignNamesWithReportingtoDesignationEmployeeNameCode(request, I, SessionDesignation)
    orgs = OrganizationList(OrganizationID)
    
    current_year = datetime.now().year
    # current_year = datetime.now().year
    years = [current_year + i for i in range(-3, 2)]

    # years = [current_year + 1, current_year, current_year - 1, current_year - 2, current_year - 3]
    selected_year = int(request.GET.get('year', current_year))
   
    context = {
        'orgs': orgs,
        'Emps':Emps,
        # 'years': years,
        # 'rowslist': rowslist,
        'I': UserOrganizationID,
        'selected_year': selected_year,
        # 'AssignYear': AssignYear,
        # 'from_year': from_year,
        # 'to_year': to_year,
        'years': years,
        'selected_employee':selected_employee
    }

    return render(request, "KRA/KraYearlyReportPrevious.html", context)


def get_kra_yearly_previous_report_json(request, organization_id, employee_code, selected_year):
    qs = KraEntryMasterDetails.objects.filter(
        KraEntryMaster__OrganizationID=organization_id,
        KraEntryMaster__SubmittedByEmployeeCode=employee_code,
        KraEntryMaster__SubmittedYear=selected_year,
        KraEntryMaster__IsDelete=False,
        IsDelete=False,
        TargetAssignMasterDetails__IsDelete=False,
    ).select_related(
        'KraEntryMaster', 'TargetAssignMasterDetails__KRA'
    ).annotate(
        Title=F('TargetAssignMasterDetails__KRA__Title'),
        Standard=F('TargetAssignMasterDetails__KRA__Standard'),
        Month=F('KraEntryMaster__SubmittedMonth'),
        Rating=F('Actual'),
    ).values('Title', 'Standard', 'Month', 'Rating', 'ActualValue')

    df = pd.DataFrame(list(qs))

    if df.empty:
        return JsonResponse([], safe=False)

    # Ensure proper types
    df['Standard'] = df['Standard'].astype(str)
    df['Title'] = df['Title'].astype(str)
    df['Month'] = df['Month'].astype(int)

    # Month mapping
    month_map = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    # Pivot each component
    pivot_rating = df.pivot_table(index=['Title'], columns='Month', values='Rating', aggfunc='first').fillna('')
    pivot_actual = df.pivot_table(index=['Title'], columns='Month', values='ActualValue', aggfunc='first').fillna('')
    pivot_standard = df.pivot_table(index=['Title'], columns='Month', values='Standard', aggfunc='first').fillna('')

    # Rename columns for clarity
    pivot_rating.rename(columns=month_map, inplace=True)
    pivot_actual.rename(columns={k: f"{v}_Actual" for k, v in month_map.items()}, inplace=True)
    pivot_standard.rename(columns={k: f"{v}_Standard" for k, v in month_map.items()}, inplace=True)

    # Merge all pivots
    final_df = pivot_rating.merge(pivot_actual, left_index=True, right_index=True)
    final_df = final_df.merge(pivot_standard, left_index=True, right_index=True)

    # Bring back the original "Standard" (as non-monthly) by getting mode of all month standards
    standard_lookup = df.groupby("Title")['Standard'].first()
    final_df.insert(1, 'Standard', final_df.index.map(standard_lookup))

    # Calculate OverallRating
    def get_overall_rating(row):
        rating_cols = [col for col in row.index if col in month_map.values()]
        values = row[rating_cols]
        counts = values[values != ''].value_counts()
        return counts.idxmax() if not counts.empty else ''

    final_df['OverallRating'] = final_df.apply(get_overall_rating, axis=1)

    # Convert to dict
    result = final_df.reset_index().to_dict(orient='records')
    return JsonResponse(result, safe=False)











# ------------------------------------------------------ Trial

def get_org_employee_list(request, ReportingtoDesignation):
    # OrganizationID always 3
    orgs = OrganizationList("3")
    all_data = []

    for org in orgs:
        org_id = org['OrganizationID']
        org_name = org['OrganizationName']

        employees = TargetAssignNames(request, org_id, ReportingtoDesignation)

        if employees:
            for emp in employees:
                all_data.append({
                    'Organization': org_name,
                    'OrganizationID': emp.OrganizationID,
                    'Employee': emp.full_name,
                    'EmployeeCode': emp.EmployeeCode,
                    'From': emp.DateofJoining.strftime('%b-%d-%Y') if emp.DateofJoining else '',
                    'To': emp.DateofLeaving.strftime('%b-%d-%Y') if hasattr(emp, 'DateofLeaving') and emp.DateofLeaving else ''
                    # 'From': emp.DateofJoining.strftime('%b-%y') if emp.DateofJoining else '',
                    # 'To': emp.DateofLeaving.strftime('%b-%y') if hasattr(emp, 'DateofLeaving') and emp.DateofLeaving else ''
                })
        else:
            # No employees for this org, still show org
            all_data.append({
                'Organization': org_name,
                'Employee': '',
                'From': '',
                'To': ''
            })

    return all_data



from django.db import transaction
from django.utils import timezone


def Bulk_TargetAssign(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    SessionEmpCode = request.session["EmployeeCode"]
    SessionDesignation = get_employee_designation_by_EmployeeCode(OrganizationID, SessionEmpCode)
    SessionEmpName = get_employee_names_by_designation(OrganizationID, SessionDesignation)
    
    
    # print("OrgID :", OrganizationID)
    # print("UserID :", UserID)
    # print("SessionEmpCode :", SessionEmpCode)
    # print("SessionDesignation :", SessionDesignation)
    # print("SessionEmpName :", SessionEmpName)

    Data = get_org_employee_list(request, SessionDesignation)


    if request.method == "POST":
        selected_rows = request.POST.getlist('rows')

        with transaction.atomic():
            for idx in selected_rows:
                emp_code  = request.POST.get(f'emp_code_{idx}')
                emp_OID   = request.POST.get(f'org_id_{idx}')
                doj       = request.POST.get(f'DOJ_{idx}')
                from_year = request.POST.get(f'FromYear_{idx}')
                to_year   = request.POST.get(f'ToYear_{idx}')

                if not all([emp_code, emp_OID, from_year, to_year]):
                    continue

                fm, fy = map(int, from_year.split('-'))
                tm, ty = map(int, to_year.split('-'))

                AssignToDesignation = get_employee_designation_by_EmployeeCode(emp_OID, emp_code)
                AssignToName = get_employee_name_by_code(emp_OID, emp_code) or "Unknown"

                # Overlap validation (same as single)
                start_new = fy * 12 + fm
                end_new   = ty * 12 + tm
                
                # print("-----------------------------------")
                # print(f"EmpCode:{emp_code} --- OID:{emp_OID} -- doj:{doj}")
                # print(f"fy:{fy} --- fm:{fm}")
                # print(f"ty:{ty} --- tm:{tm}")
                # print(f"--------")
                # print("start new:", start_new)
                # print("end new:", end_new)
                # print("-----------------------------------")


                existing = TargetAssignMaster.objects.filter(
                    IsDelete=False,
                    AssignToEmployeeCode=emp_code,
                    OrganizationID=emp_OID
                )

                for entry in existing:
                    start_existing = entry.AssignYear * 12 + entry.AssignMonth
                    end_existing   = entry.AssignToYear * 12 + entry.AssignToMonth
                    if not (end_new < start_existing or start_new > end_existing):
                        # raise ValueError(
                        #     f"Overlap found for {emp_code} in org {emp_OID}"
                        # )
                        # print(f"Overlap found for {emp_code} in org {emp_OID}")
                        continue

                # Create TargetAssignMaster
                target_assign = TargetAssignMaster.objects.create(
                    AssignByName=SessionEmpName,
                    AssignByEmployeeCode=SessionEmpCode,
                    AssignByDesignation=SessionDesignation,
                    CreatedByUserName=SessionEmpName,
                    AssignToName=AssignToName,
                    AssignDate=timezone.now().date(),
                    AssignToEmployeeCode=emp_code,
                    AssignToDesignation=AssignToDesignation,
                    AssignYear=fy,
                    AssignMonth=fm,
                    AssignToYear=ty,
                    AssignToMonth=tm,
                    AssignToDoj=doj,
                    OrganizationID=emp_OID,
                    CreatedBy=UserID,
                    CreatedDateTime=timezone.now()
                )

                # Fetch KRAs automatically
                applicable_kra_ids = HotelKRAStandard.objects.filter(
                    OrganizationID=emp_OID,
                    IsApplicable=True,
                    IsDelete=False
                ).values_list('KRAID', flat=True)

                # Assign all KRAs
                TargetAssignMasterDetails.objects.bulk_create([
                    TargetAssignMasterDetails(
                        AssignMaster=target_assign,
                        KRA_id=kra_id,
                        OrganizationID=emp_OID,
                        CreatedBy=UserID
                    )
                    for kra_id in applicable_kra_ids
                ])

        return redirect(reverse('Bulk_TargetAssign'))


    context = {
        'all_data': Data, 
        'error_message': request.GET.get('message') if request.GET.get('Success', '').lower() == 'false' else None,
    }
    return render(request, "KRA/Bulk_TargetAssign.html", context)



def KRA_Target_Report_View(request):
    current_date = datetime.now()
    OrganizationID = request.session["OrganizationID"]
    Year = int(request.GET.get('year', current_date.year))
    Month = int(request.GET.get('month_no', current_date.month))
    today = datetime.today()
    CYear = today.year
    CMonth = today.month
    context = {
        'OrganizationID':OrganizationID,
        'Year':Year,
        'CYear':range(CYear,2020,-1),
        'CMonth':CMonth,
        'Month':Month
    }
    return render(request, "KRA/KRA_Target_Report.html", context)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

class KRA_Target_Report_Api_View(APIView):
    def get(self, request):
        month = request.GET.get("month")
        year = request.GET.get("year")
        
        today = timezone.now()
        if not month or month =='':
            month = today.month
            
        if not year or year =='':
            year = today.year

        print("month is here::", month)
        print("year is here::", year)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    EXEC usp_KRA_Organization_Standard_Report
                        @year=%s
                """, [year])

                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            data = [
                dict(zip(columns, row))
                for row in rows
            ]

            return Response(
                {
                    "status": True,
                    "message": "KRA Organization Standard Report fetched successfully",
                    "data": data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


