from io import BytesIO
from django.shortcuts import render
from .models import *
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback 

# For Showing Home View
def home_view(request):
    return render(request,'check/index.html')

# For Registering The New Clerance Form
def ReferenceCheck(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    DbItemMaster = Job_Preference_Master.objects.all()
    
    ReferenceCkeckForm=forms.ReferenceCkeckForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}

    mydict={'ReferenceCkeckForm':ReferenceCkeckForm,'DbItemMaster':DbItemMaster,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        ReferenceCkeckForm=forms.ReferenceCkeckForm(request.POST,request.FILES)
        if ReferenceCkeckForm.is_valid():
         
            referenceform=ReferenceCkeckForm.save(commit=False)
            # doctor.user=user
            referenceform=referenceform.save()

            TotalItem = int((request.POST["TotalItem"]))
            for i in  range (TotalItem):
                ItemID = request.POST["ItemID_"+str(i)]
                Habits = request.POST["Habits_"+str(i)]
                
                Reference_formdetails.objects.create(
                    Habits=Habits,
                   
                    Job_Preference_Master_id=ItemID,
                    Reference_Registration_Form_id=ReferenceCkeckForm.instance.id,
                )

            
            return HttpResponseRedirect('ReferenceChecklist')
   
        
    return render(request,'check/Referencecheckform.html',context=mydict) 

#For Showing List   
def ReferenceChecklist(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    #for fetching all data from table
    OrganizationID =request.session["OrganizationID"]
    
    set_data = Reference_Registration_Form.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
    
    return render(request,"check/Referencechecklist.html",{'key1':set_data})

#For Edit the Data List
def ReferenceEditList(request):
    
       id = request.GET["id"]
       
       get_data = Reference_Registration_Form.objects.get(id=id)
       
    #    DbItemMaster = Clerance_Item_Master.objects.all()
       DbItemMaster = Reference_formdetails.objects.filter(Reference_Registration_Form_id=id).select_related('Job_Preference_Master')
       
       ReferenceCkeckForm=forms.ReferenceCkeckForm()
     
       mydict={'ReferenceCkeckForm':ReferenceCkeckForm,'Ed':get_data,'DbItemMaster':DbItemMaster}
       mydict['form']= get_data
       
       return render(request,"check/Referencecheckeditlist.html",context=mydict)
   
#For Updating the Casual Manpower Requisition Data
def UpdateReferenceForm(request):
        # print(request)
        # print(id)
        id = request.POST["ID"]
        ReferenceCkeckForm = Reference_Registration_Form.objects.get(id=id)
          
        Applicant_Name = request.POST["Applicant_Name"]
        ReferenceCkeckForm.Applicant_Name = Applicant_Name
        
        From = request.POST["From"]
        ReferenceCkeckForm.From = From
        
        To = request.POST["To"]
        ReferenceCkeckForm.To = To
        
        Referee_Company_Name = request.POST["Referee_Company_Name"]
        ReferenceCkeckForm.Referee_Company_Name = Referee_Company_Name
        
        Refeere_Name = request.POST["Refeere_Name"]
        ReferenceCkeckForm.Refeere_Name = Refeere_Name
      
        
        Did_You_Directly_Supervise = request.POST["Did_You_Directly_Supervise"]
        ReferenceCkeckForm.Did_You_Directly_Supervise = Did_You_Directly_Supervise
        
        Refeere_Position = request.POST["Refeere_Position"]
        ReferenceCkeckForm.Refeere_Position = Refeere_Position
        
        Refeere_Phone_No = request.POST["Refeere_Phone_No"]
        ReferenceCkeckForm.Refeere_Phone_No = Refeere_Phone_No
        
        Overall_Performance = request.POST["Overall_Performance"]
        ReferenceCkeckForm.Overall_Performance = Overall_Performance
        
        Strenght = request.POST["Strenght"]
        ReferenceCkeckForm.Strenght = Strenght
        
        Weaknesses = request.POST["Weaknesses"]
        ReferenceCkeckForm.Weaknesses = Weaknesses
        
        What_is_Best_Way_To_Manage_This_Candidate = request.POST["What_is_Best_Way_To_Manage_This_Candidate"]
        ReferenceCkeckForm.What_is_Best_Way_To_Manage_This_Candidate = What_is_Best_Way_To_Manage_This_Candidate
        
        What_Would_His_Supervisor_Say_About_Him = request.POST["What_Would_His_Supervisor_Say_About_Him"]
        ReferenceCkeckForm.What_Would_His_Supervisor_Say_About_Him = What_Would_His_Supervisor_Say_About_Him
        
        What_Would_His_Peers_Say_About_Him = request.POST["What_Would_His_Peers_Say_About_Him"]
        ReferenceCkeckForm.What_Would_His_Peers_Say_About_Him = What_Would_His_Peers_Say_About_Him
        
        Development_Areas = request.POST["Development_Areas"]
        ReferenceCkeckForm.Development_Areas = Development_Areas
        
        Reason_For_Leaving = request.POST["Reason_For_Leaving"]
        ReferenceCkeckForm.Reason_For_Leaving = Reason_For_Leaving
        
        Would_You_ReHire_This_Person = request.POST["Would_You_ReHire_This_Person"]
        ReferenceCkeckForm.Would_You_ReHire_This_Person = Would_You_ReHire_This_Person
        
        Checked_By = request.POST["Checked_By"]
        ReferenceCkeckForm.Checked_By = Checked_By
        
        Date = request.POST["Date"]
        ReferenceCkeckForm.Date = Date
        
        
        ReferenceCkeckForm.save()
        
        

        TotalItem = int((request.POST["TotalItem"]))
        for i in  range (TotalItem):
               
                IDs = request.POST["ID_"+str(i)]
                print(IDs)
                ItemID = request.POST["ItemID_"+str(i)]
                ReturnHabits = request.POST["Habits_"+str(i)]
                # print(ReturnHabits)
                cd = Reference_formdetails.objects.get(id=IDs)
                cd.Habits=ReturnHabits
                cd.save()
                
             
        return redirect('ReferenceChecklist')
   
   



#For Deleting The Cake Order Data
def ReferenceDeleteList(request):
       id = request.GET["id"]
  
       clerance = Reference_Registration_Form.objects.get(id=id)
       clerance.IsDelete=True;
       clerance.save();
       return redirect('ReferenceChecklist')
   

# For Showing Pdf View Of Clerance Form 
def ReferenceForm_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "check/Referencecheckviewlist.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Reference_Registration_Form.objects.get(id=id)
    
    #  ScantyBaggageForm=forms.ScantyBaggageForm()
     
     mydict={'Ed':get_data}

    # context = {'myvar': 'this is your template context','p':varM}
    
    # Create a Django response object, and specify content_type as pdf
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
    # find the template and render it.
     template = get_template(template_path)
     html = template.render(mydict)

    # create a pdf
     result = BytesIO()
    #  pisa_status = pisa.CreatePDF(
     pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        # html, dest=response, link_callback=link_callback)
    # if error then show some funny view
     if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
     return None  
