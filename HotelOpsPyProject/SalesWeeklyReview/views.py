from argparse import REMAINDER
from copyreg import remove_extension
from datetime import date
import datetime
from decimal import Decimal
from django.db import router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from SalesWeeklyReview.models import CompanyProductivityEntryDetails, CompanyProductivityEntryMaster, CompanyProductivityMaster, MarketSegmentEntryDetails, MarketSegmentEntryMaster, MarketSegmentMaster, OTAEntryDetails, OTAEntryMaster, OTAMaster, SourceEntryDetails, SourceEntryMaster, SourceMaster, TravelAgentEntryDetails, TravelAgentEntryMaster, TravelAgentMaster
from app.models import MonthListMaster
from django.db.models import Subquery
from django.db.models import OuterRef
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.db import connection
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO


def homepage(request):
    return render(request, 'SW/homepage.html' )
 
 
def  MarketSegmentList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    
    mem = MarketSegmentEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    
    return render(request, 'MarketSegment/MarketSegmentList.html' ,{'mem' :mem }) 

  
   
def MarketSegmentEntry(request):
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
        Total = request.POST["Total"]
        TotalRevenue = request.POST["TotalRevenue"]
        TotalADR = request.POST["TotalADR"]
        enmaster= MarketSegmentEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,Total=Total,
                                    TotalRevenue=TotalRevenue,TotalADR=TotalADR ,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            RoomNights = request.POST["RoomNights_" + str(x)]
            if(RoomNights == ''):
                RoomNights = 0
            Revenue = request.POST["Revenue_" + str(x)]
            if(Revenue == ''):
                Revenue = 0
            ADR = request.POST["ADR_" + str(x)]
            if(ADR == ''):
                ADR = 0
                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=MarketSegmentMaster.objects.get(id=TitleID_)
            EntOBj=MarketSegmentEntryMaster.objects.get(id=enmaster.pk)
              
            v = MarketSegmentEntryDetails.objects.create(RoomNights = RoomNights,Revenue=Revenue, ADR=ADR,
                                                       MarketSegmentMaster=TitleObje,
                                                       MarketSegmentEntryMaster= EntOBj
                                                      )                        
        return(redirect('/SalesWeeklyReview/MarketSegmentList'))
    mem = MarketSegmentMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'MarketSegment/MarketSegmentEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def delete_MarketSegment (request,id):
    mem = MarketSegmentEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/SalesWeeklyReview/MarketSegmentList'))



def MarketSegmentEdit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        Total = request.POST["Total"]
        TotalRevenue = request.POST["TotalRevenue"]
        TotalADR = request.POST["TotalADR"]
        
        mem = MarketSegmentEntryMaster.objects.get(id = id)            
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear
        mem.Total = Total
        mem.TotalRevenue = TotalRevenue
        mem.TotalADR = TotalADR
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            RoomNights = request.POST["RoomNights_" + str(x)]
            Revenue = request.POST["Revenue_" + str(x)]
            ADR = request.POST["ADR_" + str(x)]
        
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = MarketSegmentEntryMaster.objects.get(id = id)
              
            sv = MarketSegmentEntryDetails.objects.get( MarketSegmentEntryMaster = id , MarketSegmentMaster = TitleID_)
            sv.RoomNights = RoomNights
            sv.Revenue = Revenue
            sv.ADR = ADR
            sv.save()
                                                        
        return(redirect('/SalesWeeklyReview/MarketSegmentList'))   
    mem1 = MarketSegmentEntryDetails.objects.filter(MarketSegmentEntryMaster=id,IsDelete = False).select_related("MarketSegmentMaster")
    mem = MarketSegmentEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'MarketSegment/MarketSegmentEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })



def MarketSegmentviewdata(request , id):
  
    template_path = "MarketSegment/MarketSegmentviewdata.html"
 
    mem1 = MarketSegmentEntryDetails.objects.filter(MarketSegmentEntryMaster=id,IsDelete = False).select_related("MarketSegmentMaster")
    mem = MarketSegmentEntryMaster.objects.get(id = id)
    
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




 
def  SourceList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = SourceEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'Source/SourceList.html' ,{'mem' :mem }) 
from django.db.models import Q   
def SourceEntry(request):
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
        Total = request.POST["Total"]
        TotalRevenue = request.POST["TotalRevenue"]
        TotalADR = request.POST["TotalADR"]
        TotalRPD= request.POST["TotalRPD"]
        
        enmaster= SourceEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,Total=Total,
                                                   TotalRevenue=TotalRevenue,
                                                   TotalADR=TotalADR,
                                                   TotalRPD=TotalRPD,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            RMNights = request.POST["RMNights_" + str(x)]
            if(RMNights == ''):
                RMNights = 0
            Revenue = request.POST["Revenue_" + str(x)]
            if(Revenue == ''):
                Revenue = 0
            ADR = request.POST["ADR_" + str(x)]
            if(ADR == ''):
                ADR = 0
            RPD = request.POST["RPD_" + str(x)]
            if(RPD ==''):
                RPD = 0
                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=SourceMaster.objects.get(id=TitleID_)
            EntOBj=SourceEntryMaster.objects.get(id=enmaster.pk)
              
            v = SourceEntryDetails.objects.create(RMNights = RMNights,Revenue=Revenue, ADR=ADR, RPD=RPD,
                                                       SourceMaster=TitleObje,
                                                       SourceEntryMaster= EntOBj
                                                      )                        
        return(redirect('/SalesWeeklyReview/SourceList'))
    mem = SourceMaster.objects.filter(Q(IsDelete=False) & (Q(OrganizationID=0) | Q(OrganizationID=OrganizationID)))    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'Source/SourceEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def delete_Source (request,id):
    mem = SourceEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/SalesWeeklyReview/SourceList'))



def SourceEdit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        Total = request.POST["Total"]
        TotalRevenue = request.POST["TotalRevenue"]
        TotalADR = request.POST["TotalADR"]
        TotalRPD = request.POST["TotalRPD"]
        
        mem = SourceEntryMaster.objects.get(id = id)            
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear
        mem.Total = Total
        mem.TotalRevenue = TotalRevenue
        mem.TotalADR = TotalADR
        mem.TotalRPD = TotalRPD
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            RMNights = request.POST["RMNights_" + str(x)]
            Revenue = request.POST["Revenue_" + str(x)]
            ADR = request.POST["ADR_" + str(x)]
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = SourceEntryMaster.objects.get(id = id)
              
            sv = SourceEntryDetails.objects.get( SourceEntryMaster = id , SourceMaster = TitleID_)
            sv.RMNights = RMNights
            sv.Revenue = Revenue
            sv.ADR = ADR
            sv.save()
                                                        
        return(redirect('/SalesWeeklyReview/SourceList'))   
    mem1 = SourceEntryDetails.objects.filter(SourceEntryMaster=id,IsDelete = False).select_related("SourceMaster")
    mem = SourceEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'Source/SourceEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })


def SourceView(request , id):
  
    template_path = "Source/Sourceviewdata.html"
 
    mem1 = SourceEntryDetails.objects.filter(SourceEntryMaster=id,IsDelete = False).select_related("SourceMaster")
    mem = SourceEntryMaster.objects.get(id = id)
    
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



 
def  OTAList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = OTAEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'OTAReport/OTAList.html' ,{'mem' :mem })   

def OTAEntry(request):
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
        Total = request.POST["Total"]
        TotalRevenue = request.POST["TotalRevenue"]
        TotalARR = request.POST["TotalARR"]
        TotalRPD = request.POST["TotalRPD"]
        enmaster= OTAEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,Total=Total,
                                    TotalRevenue=TotalRevenue,TotalARR=TotalARR,TotalRPD=TotalRPD,
                                    OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            RoomNights = request.POST["RoomNights_" + str(x)]
            if(RoomNights == ''):
                RoomNights = 0
            RoomRevenue = request.POST["RoomRevenue_" + str(x)]
            if(RoomRevenue == ''):
                RoomRevenue = 0
            ARR = request.POST["ARR_" + str(x)]
            if(ARR == ''):
                ARR = 0
            RPD = request.POST["RPD_" + str(x)]
            if(RPD ==''):
                RPD = 0
                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=OTAMaster.objects.get(id=TitleID_)
            EntOBj=OTAEntryMaster.objects.get(id=enmaster.pk)
              
            v = OTAEntryDetails.objects.create( RoomNights = RoomNights, RoomRevenue=RoomRevenue,
                                                       ARR=ARR,
                                                       RPD=RPD,
                                                       OTAMaster=TitleObje,
                                                       OTAEntryMaster= EntOBj
                                                      )                        
        return(redirect('/SalesWeeklyReview/OTAList'))
    mem = OTAMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'OTAReport/OTAEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def delete_OTA (request,id):
    mem = OTAEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/SalesWeeklyReview/OTAList'))


def OTAEdit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        Total = request.POST["Total"]
        TotalRevenue = request.POST["TotalRevenue"]
        TotalARR = request.POST["TotalARR"]
        TotalRPD = request.POST["TotalRPD"]
        
        mem = OTAEntryMaster.objects.get(id = id)            
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear
        mem.Total = Total
        mem.TotalRevenue = TotalRevenue
        mem.TotalARR = TotalARR
        mem.TotalRPD = TotalRPD
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            RoomNights = request.POST["RoomNights_" + str(x)]
            RoomRevenue = request.POST["RoomRevenue_" + str(x)]
            ARR = request.POST["ARR_" + str(x)]
            RPD = request.POST["RPD_" + str(x)]
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = OTAEntryMaster.objects.get(id = id)
              
            sv = OTAEntryDetails.objects.get( OTAEntryMaster = id , OTAMaster = TitleID_)
            sv.RoomNights = RoomNights
            sv.RoomRevenue = RoomRevenue
            sv.ARR = ARR
            sv.RPD = RPD
            sv.save()
                                                        
        return(redirect('/SalesWeeklyReview/OTAList'))   
    mem1 = OTAEntryDetails.objects.filter(OTAEntryMaster=id,IsDelete = False).select_related("OTAMaster")
    mem = OTAEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'OTAReport/OTAEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })


def OTAView(request , id):
  
    template_path = "OTAReport/OTAviewdata.html"
 
    mem1 = OTAEntryDetails.objects.filter(OTAEntryMaster=id,IsDelete = False).select_related("OTAMaster")
    mem = OTAEntryMaster.objects.get(id = id)
    
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




 
def  TravelAgentList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = TravelAgentEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'TravelAgentProductivity/TravelAgentList.html' ,{'mem' :mem })   


def TravelAgentEntry(request):
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
        enmaster= TravelAgentEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            RoomNights = request.POST["RoomNights_" + str(x)]
            if(RoomNights == ''):
                RoomNights = 0
            RoomRevenue = request.POST["RoomRevenue_" + str(x)]
            if(RoomRevenue == ''):
                RoomRevenue = 0
            ARR = request.POST["ARR_" + str(x)]
            if(ARR == ''):
                ARR = 0

                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=TravelAgentMaster.objects.get(id=TitleID_)
            EntOBj=TravelAgentEntryMaster.objects.get(id=enmaster.pk)
              
            v = TravelAgentEntryDetails.objects.create( RoomNights = RoomNights, RoomRevenue=RoomRevenue,
                                                       ARR=ARR,
                                                       TravelAgentMaster=TitleObje,
                                                       TravelAgentEntryMaster= EntOBj
                                                      )                        
        return(redirect('/SalesWeeklyReview/TravelAgentList'))
    mem = TravelAgentMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'TravelAgentProductivity/TravelAgentEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def delete_TravelAgent (request,id):
    mem = TravelAgentEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/SalesWeeklyReview/TravelAgentList'))

def TravelAgentEdit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
             
        mem = TravelAgentEntryMaster.objects.get(id = id)            
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear     
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            RoomNights = request.POST["RoomNights_" + str(x)]
            RoomRevenue = request.POST["RoomRevenue_" + str(x)]
            ARR = request.POST["ARR_" + str(x)]
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = TravelAgentEntryMaster.objects.get(id = id)
              
            sv = TravelAgentEntryDetails.objects.get( TravelAgentEntryMaster = id , TravelAgentMaster = TitleID_)
            sv.RoomNights = RoomNights
            sv.RoomRevenue = RoomRevenue
            sv.ARR = ARR
            sv.save()
                                                        
        return(redirect('/SalesWeeklyReview/TravelAgentList'))   
    mem1 = TravelAgentEntryDetails.objects.filter(TravelAgentEntryMaster=id,IsDelete = False).select_related("TravelAgentMaster")
    mem = TravelAgentEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'TravelAgentProductivity/TravelAgentEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })


def TravelAgentView(request , id):
  
    template_path = "TravelAgentProductivity/TravelAgentviewdata.html"
 
    mem1 = TravelAgentEntryDetails.objects.filter(TravelAgentEntryMaster=id,IsDelete = False).select_related("TravelAgentMaster")
    mem = TravelAgentEntryMaster.objects.get(id = id)
    
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


 
 
def  CompanyProList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = CompanyProductivityEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'CompanyProductivity/CompanyProList.html' ,{'mem' :mem })   

def CompanyProEntry(request):
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
        enmaster= CompanyProductivityEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            RoomNights = request.POST["RoomNights_" + str(x)]
            if(RoomNights == ''):
                RoomNights = 0
            RoomRevenue = request.POST["RoomRevenue_" + str(x)]
            if(RoomRevenue == ''):
                RoomRevenue = 0
            ARR = request.POST["ARR_" + str(x)]
            if(ARR == ''):
                ARR = 0

                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=CompanyProductivityMaster.objects.get(id=TitleID_)
            EntOBj=CompanyProductivityEntryMaster.objects.get(id=enmaster.pk)
              
            v = CompanyProductivityEntryDetails.objects.create( RoomNights = RoomNights, RoomRevenue=RoomRevenue,
                                                       ARR=ARR,
                                                       CompanyProductivityMaster=TitleObje,
                                                       CompanyProductivityEntryMaster= EntOBj
                                                      )                        
        return(redirect('/SalesWeeklyReview/CompanyProList'))
    mem = CompanyProductivityMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'CompanyProductivity/CompanyProEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def delete_CompanyPro (request,id):
    mem = CompanyProductivityEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/SalesWeeklyReview/CompanyProList'))


def CompanyProEdit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
             
        mem = CompanyProductivityEntryMaster.objects.get(id = id)            
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear     
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            RoomNights = request.POST["RoomNights_" + str(x)]
            RoomRevenue = request.POST["RoomRevenue_" + str(x)]
            ARR = request.POST["ARR_" + str(x)]
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = CompanyProductivityEntryMaster.objects.get(id = id)
              
            sv = CompanyProductivityEntryDetails.objects.get( CompanyProductivityEntryMaster = id , CompanyProductivityMaster = TitleID_)
            sv.RoomNights = RoomNights
            sv.RoomRevenue = RoomRevenue
            sv.ARR = ARR
            sv.save()
                                                        
        return(redirect('/SalesWeeklyReview/CompanyProList'))   
    mem1 = CompanyProductivityEntryDetails.objects.filter(CompanyProductivityEntryMaster=id,IsDelete = False).select_related("CompanyProductivityMaster")
    mem = CompanyProductivityEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'CompanyProductivity/CompanyProEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })


def CompanyProView(request , id):
  
    template_path = "CompanyProductivity/CompanyProviewdata.html"
 
    mem1 = CompanyProductivityEntryDetails.objects.filter(CompanyProductivityEntryMaster=id,IsDelete = False).select_related("CompanyProductivityMaster")
    mem = CompanyProductivityEntryMaster.objects.get(id = id)
    
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

