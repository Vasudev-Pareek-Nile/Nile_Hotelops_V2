from argparse import REMAINDER
from copyreg import remove_extension
from datetime import date
from datetime import datetime
# import datetime
from decimal import Decimal
# import xdrlib
from django.db import router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
import requests
from PreOpeningDoc.models import DivisionMaster
from PreOpeningDoc.models import  FixedSignageEntryDetails, FixedSignageEntryMaster, FixedSignageMaster, HandOverEntryDetails, HotelHandOverEntryMaster, HotelHandOverMaster, IndicativeProImpEntryDetails, IndicativeProImpEntryMaster, IndicativeProImpMaster, ProjectImpProcessEntryDetails, ProjectImpProcessEntryMaster, ProjectImpProcessMaster, SectionMaster, SnagListEntryDetails, SnagListEntryMaster, SnagListMaster
from app.models import MonthListMaster
from django.db.models import Subquery
from django.db.models import OuterRef
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.db import connection
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO

xdrlib=""

def homepage(request):
    return render(request, 'POD/homepage.html' )

 
def  FixedSigList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = FixedSignageEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'FixedSignage/FixedSigList.html' ,{'mem' :mem }) 

    
def FixedSigEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"] 
        EntryYear = request.POST["EntryYear"] 
        
        enmaster= FixedSignageEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,
                                     OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()              
                              
        TitleID_ = request.POST["TitleID_" + str(xdrlib)]
            
        TitleObje=FixedSignageMaster.objects.get(id=TitleID_)
        EntOBj=FixedSignageEntryMaster.objects.get(id=enmaster.pk)
              
        v = FixedSignageEntryDetails.objects.create( FixedSignageMaster=TitleObje,
                                                       FixedSignageEntryMaster= EntOBj )  
                                 
        return(redirect('/PreOpeningDoc/FixedSigList'))
    mem = FixedSignageMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'FixedSignage/FixedSigEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})



def  ProImpPlanList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = IndicativeProImpEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'ProjimpPlan/ProimpList.html' ,{'mem' :mem }) 

   
def ProImpPlanEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"] 
        EntryYear = request.POST["EntryYear"] 
        Months = request.POST["Months"]
        TotalIndProjTimeFrame = request.POST["TotalIndProjTimeFrame"]
        
        enmaster= IndicativeProImpEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,Months=Months,
                        TotalIndProjTimeFrame=TotalIndProjTimeFrame, OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()              
                              
        TitleID_ = request.POST["TitleID_" + str(xdrlib)]
            
        TitleObje=IndicativeProImpMaster.objects.get(id=TitleID_)
        EntOBj=IndicativeProImpEntryMaster.objects.get(id=enmaster.pk)
              
        v = IndicativeProImpEntryDetails.objects.create( IndicativeProImpMaster=TitleObje,
                                                       IndicativeProImpEntryMaster= EntOBj )  
                                 
        return(redirect('/PreOpeningDoc/ProImpPlanList'))
    mem = IndicativeProImpMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'ProjimpPlan/ProImpEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def  ProImpProcessList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = ProjectImpProcessEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'ProjectimpProcess/ProjectimpList.html' ,{'mem' :mem }) 


   
def ProImpProcessEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        Project = request.POST["Project"] 
        StartDate = request.POST["StartDate"] 
        ForecastCompletionDate = request.POST["ForecastCompletionDate"]
        Attention = request.POST["Attention"]
        Issue = request.POST["Issue"]
        By = request.POST["By"]
        Date = request.POST["Date"]
        enmaster= ProjectImpProcessEntryMaster.objects.create(Project=Project,StartDate=StartDate,ForecastCompletionDate=ForecastCompletionDate,
                                    Attention=Attention,Issue=Issue ,By=By,Date=Date,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            ResponseTime = request.POST["ResponseTime_" + str(x)]
            if(ResponseTime == ''):
                ResponseTime = 0
            CompletionBy = request.POST["CompletionBy_" + str(x)]
            if(CompletionBy == ''):
                CompletionBy = 0
            Remarks = request.POST["Remarks_" + str(x)]
            if(Remarks == ''):
                Remarks = 0
                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=ProjectImpProcessMaster.objects.get(id=TitleID_)
            EntOBj=ProjectImpProcessEntryMaster.objects.get(id=enmaster.pk)
              
            v = ProjectImpProcessEntryDetails.objects.create(ResponseTime = ResponseTime,CompletionBy=CompletionBy, Remarks=Remarks,
                                                       ProjectImpProcessMaster=TitleObje,
                                                       ProjectImpProcessEntryMaster= EntOBj
                                                      )                        
        return(redirect('/PreOpeningDoc/ProImpProcessList'))
    mem = ProjectImpProcessMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'ProjectimpProcess/ProjectimpEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})



def ProImpProcessEdit(request , id):
    if request.method == "POST":
        Project = request.POST["Project"]
        StartDate = request.POST["StartDate"]
        ForecastCompletionDate = request.POST["ForecastCompletionDate"]
        Attention = request.POST["Attention"]
        Issue = request.POST["Issue"]
        By = request.POST["By"]
        Date = request.POST["Date"]
        
        mem = ProjectImpProcessEntryMaster.objects.get(id = id)            
        mem.Project = Project
        mem.StartDate =StartDate
        mem.ForecastCompletionDate = ForecastCompletionDate
        mem.Attention = Attention
        mem.Issue = Issue
        mem.By = By
        mem.Date = Date
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            ResponseTime = request.POST["ResponseTime_" + str(x)]
            CompletionBy = request.POST["CompletionBy_" + str(x)]
            Remarks = request.POST["Remarks_" + str(x)]
        
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = ProjectImpProcessEntryMaster.objects.get(id = id)
              
            sv = ProjectImpProcessEntryDetails.objects.get( ProjectImpProcessEntryMaster = id , ProjectImpProcessMaster = TitleID_)
            sv.ResponseTime = ResponseTime
            sv.CompletionBy = CompletionBy
            sv.Remarks = Remarks
            sv.save()
                                                        
        return(redirect('/PreOpeningDoc/ProImpProcessList'))   
    mem1 = ProjectImpProcessEntryDetails.objects.filter(ProjectImpProcessEntryMaster=id,IsDelete = False).select_related("ProjectImpProcessMaster")
    mem = ProjectImpProcessEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'ProjectimpProcess/ProjectimpEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })

def delete_ProImpProcess (request,id):
    mem = ProjectImpProcessEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/PreOpeningDoc/ProImpProcessList'))


def ProImpProcessView(request , id):
  
    template_path = "ProjectimpProcess/ProjectimpView.html"
 
    mem1 = ProjectImpProcessEntryDetails.objects.filter(ProjectImpProcessEntryMaster=id,IsDelete = False).select_related("ProjectImpProcessMaster")
    mem = ProjectImpProcessEntryMaster.objects.get(id = id)
    
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
   
    template = get_template(template_path)
    html = template.render(mydict)
    
    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
  
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



def  HotelHandoverList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = HotelHandOverEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'HotelHandover/HotelHandoverList.html' ,{'mem' :mem }) 


   
def HotelHandoverEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        WeeksBefore = request.POST["WeeksBefore"] 
        Remarks = request.POST["Remarks"] 
    
        enmaster= HotelHandOverEntryMaster.objects.create(WeeksBefore=WeeksBefore, Remarks=Remarks,
                                   OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            WeeksBefore = request.POST["WeeksBefore_" + str(x)]
            if(WeeksBefore == ''):
                WeeksBefore = 0
            Remarks = request.POST["Remarks_" + str(x)]
            if(Remarks == ''):
                Remarks = 0
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=HotelHandOverMaster.objects.get(id=TitleID_)
            EntOBj=HotelHandOverEntryMaster.objects.get(id=enmaster.pk)
              
            v = HandOverEntryDetails.objects.create(WeeksBefore = WeeksBefore, Remarks=Remarks,
                                                       HotelHandOverMaster=TitleObje,
                                                       HotelHandOverEntryMaster= EntOBj
                                                      )                        
        return(redirect('/PreOpeningDoc/HotelHandoverList'))
    mem = HotelHandOverMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'HotelHandover/HotelHandoverEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def  SnagList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = SnagListEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').all()     
    return render(request, 'SnagList/SnagList.html' ,{'mem' :mem }) 
   

   
def SnagEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    CreatedBy=UserID
    mem = DivisionMaster.objects.filter(IsDelete = False)    
    return render(request, 'SnagList/SnagEntry.html' ,{'mem':mem,})

  
def SnagSectionEntry(request,id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    CreatedBy=UserID
    mem = SectionMaster.objects.filter(IsDelete = False,DivisionMaster=id).select_related('DivisionMaster')  
    return render(request, 'SnagList/SnagSectionEntry.html' ,{'mem':mem,})


def SnagListEntry(request,id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    objSM = get_object_or_404(SectionMaster, pk=id)
    if request.method == "POST":
        Area = request.POST["Area"]
        Date = request.POST["Date"]
        # Parse the original date string to a datetime object
        original_date = datetime.strptime(Date, '%d-%B-%y')

        # Convert the datetime object to the desired format
        formatted_date = original_date.strftime('%Y-%m-%d')
        
      
        enmaster= SnagListEntryMaster.objects.create(SectionMaster=objSM,Area=Area,  Date=formatted_date,
                        OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()              
                                                     
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)):  
            Yes = request.POST.get("Yes_"+str(x),'False')
            if (Yes == True):
                Yes = True
            else:
                Yes = False
            Remarks = request.POST.get("Remarks_"+str(x),'')
            if (Remarks == ''):
                Remarks = 0                   
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
                
            TitleObje=SnagListMaster.objects.get(id=TitleID_)
            EntOBj=SnagListEntryMaster.objects.get(id=enmaster.pk)
                
            v = SnagListEntryDetails.objects.create( SnagListMaster=TitleObje, Yes = Yes , Remarks=Remarks,OrganizationID=OrganizationID,CreatedBy=UserID,
                                                        SnagListEntryMaster= EntOBj )                                   
        return(redirect('/PreOpeningDoc/SnagList'))
    print(id)
    mem = SnagListMaster.objects.filter(IsDelete = False,SectionMaster=id)
  
    # mem = SectionMaster.objects.filter(IsDelete = False,DivisionMaster=id).select_related('DivisionMaster')  
    return render(request, 'SnagList/SnagListEntry.html' ,{'mem':mem,'id':id})


def delete_SnagList (request,id):
    mem = SnagListEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/PreOpeningDoc/SnagList'))


def SnagListEdit(request , id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    if request.method == "POST":
        Area = request.POST["Area"]
        Date = request.POST["Date"]  
             
        mem = SnagListEntryMaster.objects.get(id = id)            
        mem.Area = Area
        mem.Date = Date
        mem.ModifyBy=UserID
        mem.ModifyDateTime=datetime.now()
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)):
            
            Yes = request.POST.get("Yes_" + str(x),False)
            Remarks = request.POST.get("Remarks_" + str(x),'')
        
            TitleID_ = request.POST["TitleID_" + str(x)]
            mID = request.POST["ID_" + str(x)]
            mem1 = SnagListEntryMaster.objects.get(id = id)
              
            sv  = SnagListEntryDetails.objects.get(SnagListMaster = TitleID_,id=mID)  # SnagListEntryDetails.objects.get( SnagListEntryMaster = id , SnagListMaster = TitleID_)
            sv.Yes = Yes
            sv.Remarks = Remarks
            sv.ModifyBy=UserID
            sv.ModifyDateTime=datetime.now()
            sv.save()                                                        
        return(redirect('/PreOpeningDoc/SnagList'))   
    mem1 = SnagListEntryDetails.objects.filter(SnagListEntryMaster=id,IsDelete = False).all()
    print(mem1)
        # Access related SnagListEntryDetails along with their SectionMaster and DivisionMaster
    mem = SnagListEntryMaster.objects.get(id = id)
    return render(request,'SnagList/SnagListEdit.html',{'mem':mem , 'mem1':mem1 })



    
def SectionMasterList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mem = SectionMaster.objects.filter(IsDelete = False).select_related('DivisionMaster')    
    
    return render(request, 'SnagList/SectionMasterList.html' ,{'mem':mem})


def SectionMasterEntry(request ) :
    if request.method == 'POST':
        strDivision  =request.POST["Division"]
        objDi =  get_object_or_404(DivisionMaster, pk=strDivision)
        strSection  =request.POST["Section"]
        se= SectionMaster.objects.create(title=strSection,DivisionMaster=objDi)

        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)):  
            # Category = request.POST["Category_"+str(x)]
            Category= request.POST.get("Category_"+str(x), '')
            if (Category == "True"):
                Category = "1"
            else:
                Category="0"
            Title = request.POST["Title["+str(x)+"]"]
            WorkType = request.POST["WorkType_"+str(x)+""]
            

            v = SnagListMaster.objects.create( SectionMaster=se, category = Category , title=Title,worktype=WorkType ) 
        

    else:
     form = SectionMaster.objects.filter(IsDelete = False)
     dl = DivisionMaster.objects.filter(IsDelete = False)
    
     return render(request , 'SnagList/SectionEntry.html' , {'form' : form,'dl':dl})
    
    return(redirect('/PreOpeningDoc/SectionMasterList'))
    

def SectionMasterEdit(request , id) :
    obj =  get_object_or_404(SectionMaster, pk=id)
    dl = DivisionMaster.objects.filter(IsDelete = False)
    if request.method == 'POST':
            strtile = request.POST["Section"]
            strDivi = request.POST["Division"]
            objDi =  get_object_or_404(DivisionMaster, pk=strDivi)
            obj.title=strtile;
            obj.DivisionMaster=objDi;
            obj.save();

            TotalItem = request.POST["TotalItem"]
            for x in range(int(TotalItem)):  
                # Category = request.POST["Category_"+str(x)]
                Category= request.POST.get("Category_"+str(x), '')
                if (Category == "True"):
                    Category = "1"
                else:
                    Category="0"
                Title = request.POST.get("Title["+str(x)+"]")
                id = request.POST.get("id["+str(x)+"]")
                WorkType = request.POST["WorkType_"+str(x)+""]

                print(id)
                if int(id)<1:
                    v = SnagListMaster.objects.create( SectionMaster=obj, category = Category , title=Title ,worktype=WorkType) 
                else:
                    v =get_object_or_404(SnagListMaster, pk=id) 
                    v.title=Title;
                    v.category=Category;
                    v.worktype= WorkType;
                    v.save()
            return redirect('SectionMasterList')
    else:
     form = SectionMaster.objects.filter(IsDelete = False,id=id)
     Snl = SnagListMaster.objects.filter(IsDelete = False,SectionMaster=obj)
     return render(request , 'SnagList/SectionMasterEdit.html' , {'form' : obj,'dl':dl,'Snl':Snl})
    
    return(redirect('/PreOpeningDoc/DivisonMasterList'))
   


def delete_Section (request,id):
    mem = SectionMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/PreOpeningDoc/SectionMasterList'))



def DivisonMasterList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"] 
        EntryYear = request.POST["EntryYear"] 
        
        enmaster= FixedSignageEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,
                                     OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()              
                              
        TitleID_ = request.POST["TitleID_" + str(xdrlib)]
            
        TitleObje=FixedSignageMaster.objects.get(id=TitleID_)
        EntOBj=FixedSignageEntryMaster.objects.get(id=enmaster.pk)
              
        v = FixedSignageEntryDetails.objects.create( FixedSignageMaster=TitleObje,
                                                       FixedSignageEntryMaster= EntOBj )  
                                 
        return(redirect('/PreOpeningDoc/SnagList'))
    mem = DivisionMaster.objects.filter(IsDelete = False)    
    today = date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'SnagList/DivisonMasterList.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})



def DivisionEntry(request ) :
    if request.method == 'POST':
        strDivision  =request.POST["Division"]
        DivisionMaster.objects.create(title=strDivision)
    else:
     form = DivisionMaster.objects.filter(IsDelete = False)
     return render(request , 'SnagList/DivisionEntry.html' , {'form' : form})
    
    return(redirect('/PreOpeningDoc/DivisonMasterList'))
    

def DivisonEdit(request , id) :
    obj =  get_object_or_404(DivisionMaster, pk=id)
    if request.method == 'POST':
            strtile = request.POST["Division"]
            obj.title=strtile;
            obj.save();
            return redirect('DivisonMasterList')
    else:
     form = DivisionMaster.objects.filter(IsDelete = False,id=id)
     return render(request , 'SnagList/DivisonEdit.html' , {'form' : obj})
    
    return(redirect('/PreOpeningDoc/DivisonMasterList'))
   
 
def delete_Divison (request,id):
    mem = DivisionMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/PreOpeningDoc/DivisonMasterList'))
   

def  ReportPendingTask(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    current_year = datetime.now().year
    years = range(2022, current_year + 1)


    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
    'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        mem = response.json()
      #  return JsonResponse(mem)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    I=""
    if 'I' in request.GET:
        I=request.GET["I"]
    else:
        I = OrganizationID

    worktype=""
    if 'worktype' in request.GET:
        worktype=request.GET["worktype"]
    

    Expapi_url = "https://hotelops.in/API/PyPreOpeningDocAPI/PreOpeningDoc_SP_SnagList_Report_PendingTask?OrganizationID="+str(I)+"&worktype="+str(worktype)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(Expapi_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        DataRes = response.json()
      #  return JsonResponse(mem)
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    context = {'years': years,'mem':mem,'DataRes':DataRes}

    return render(request, 'SnagList/ReportPendingTask.html' ,context) 



def  ReportPendingTaskExport(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    current_year = datetime.now().year
    years = range(2022, current_year + 1)


    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
    'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        mem = response.json()
      #  return JsonResponse(mem)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    I=""
    if 'I' in request.GET:
        I=request.GET["I"]
    else:
        I = OrganizationID

    worktype=""
    if 'worktype' in request.GET:
        worktype=request.GET["worktype"]
    

    Expapi_url = "https://hotelops.in/API/PyPreOpeningDocAPI/PreOpeningDoc_SP_SnagList_Report_PendingTask?OrganizationID="+str(I)+"&worktype="+str(worktype)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(Expapi_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        DataRes = response.json()
      #  return JsonResponse(mem)
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    context = {'years': years,'mem':mem,'DataRes':DataRes}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
# find the template and render it.
    template_path="SnagList/ReportPendingTaskExport.html"
    template = get_template(template_path)
    html = template.render(context)
    header_html = '''
        <div style="position: fixed; top: 0;">
            <!-- Your header content here -->
            <h1>Header Content</h1>
        </div>
    '''
    html = header_html + html
# create a pdf
    result = BytesIO()
#  pisa_status = pisa.CreatePDF(
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # html, dest=response, link_callback=link_callback)
# if error then show some funny view
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 
    return render(request, 'SnagList/ReportPendingTaskExport.html' ,context) 

    