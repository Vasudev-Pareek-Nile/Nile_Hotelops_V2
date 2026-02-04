from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import  Project_Approvel_Request,Contract_summary,owners,Project,Contract_deta,owner_deta,project_deta,Opportunityss

# Create your views here.
def Project_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    Contract = Contract_summary.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    ownes = owners.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    project = Project.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    Oppo = Opportunityss.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    Appro_id = request.GET.get('ID')
    Appro = None
    if Appro_id is not None:
        Appro = get_object_or_404(Project_Approvel_Request,id=Appro_id,OrganizationID=OrganizationID)
    if request.method=="POST":
        if Appro_id is not None:
                Appro.Hotel_type = request.POST['Hotel_type']
                Appro.Strategy=request.POST['Strategy']
                Appro.Development_type=request.POST['Development_type']
                Appro.Status=request.POST['Status']
                Appro.Opening_Date=request.POST['Opening_Date']
                Appro.RHG_Contribution=request.POST['RHG_Contribution']
                Appro.Fee_income=request.POST['Fee_income']
                Appro.IRR_applicable=request.POST['IRR_applicable']
            
                Appro.Location=request.POST['Location']
                Appro.Location_label=request.POST['Location_label']
                Appro.Location_type=request.POST['Location_type']
                Appro.Rooms=request.POST['Rooms']
                Appro.FB_outlets=request.POST['FB_outlets']
                Appro.MeetingCoWork=request.POST['MeetingCoWork']
                Appro.Other=request.POST['Other']
                
                Appro.adr_fv=request.POST['adr_fv']
                Appro.adr_pv=request.POST['adr_pv']
                Appro.occ=request.POST['occ']
                Appro.rav_fv=request.POST['rav_fv']
                Appro.rev_pv=request.POST['rev_pv']
                Appro.rrev=request.POST['rrev']
                Appro.term=request.POST['term']
                Appro.in_rate=request.POST['in_rate']
                Appro.royalty_fee1=request.POST['royalty_fee1']
                Appro.royalty_fee2=request.POST['royalty_fee2']
                Appro.zma_fee1=request.POST['zma_fee1']
                Appro.zma_fee2=request.POST['zma_fee2']
                Appro.total_fee1=request.POST['total_fee1']
                Appro.total_fee2=request.POST['total_fee2']
                Appro.total_fee3=request.POST['total_fee3']
                Appro.meur=request.POST['meur']
                Appro.yp1=request.POST['yp1']
                Appro.yp2=request.POST['yp2']
                Appro.year1=request.POST['year1']
                Appro.year2=request.POST['year2']
                Appro.year3=request.POST['year3']
                Appro.occ1=request.POST['occ1']
                Appro.rc1=request.POST['rc1']
                Appro.old_rev1=request.POST['old_rev1']
                Appro.occ2=request.POST['occ2']
                Appro.rc2=request.POST['rc2']
                Appro.old_rev2=request.POST['old_rev2']
                Appro.occ3=request.POST['occ3']
                Appro.rc3=request.POST['rc3']
                Appro.old_rev3=request.POST['old_rev3']
                Appro.totalocc=request.POST['totalocc']
                Appro.totalrc=request.POST['totalrc']
                Appro.total_rev=request.POST['total_rev']

                Appro.com_occ1=request.POST['com_occ1']
                Appro.com_adr1=request.POST['com_adr1']
                Appro.com_rev1=request.POST['com_rev1']
                Appro.com_occ2=request.POST['com_occ2']
                Appro.com_adr2=request.POST['com_adr2']
                Appro.com_rev2=request.POST['com_rev2']
                Appro.com_occ3=request.POST['com_occ3']
                Appro.com_adr3=request.POST['com_adr3']
                Appro.com_rev3=request.POST['com_rev3']
                Appro.totalcom_occ=request.POST['totalcom_occ']
                Appro.totalcom_adr=request.POST['totalcom_adr']
                Appro.totalcom_rev=request.POST['totalcom_rev']
                
                Appro.pro_occ1=request.POST['pro_occ1']
                Appro.pro_adr1=request.POST['pro_adr1']
                Appro.pro_rev1=request.POST['pro_rev1']
                Appro.pro_occ2=request.POST['pro_occ2']
                Appro.pro_adr2=request.POST['pro_adr2']
                Appro.pro_rev2=request.POST['pro_rev2']
                Appro.pro_occ3=request.POST['pro_occ3']
                Appro.pro_adr3=request.POST['pro_adr3']
                Appro.pro_rev3=request.POST['pro_rev3']
                Appro.total_pro_occ=request.POST['total_pro_occ']
                Appro.totalpro_adr=request.POST['totalpro_adr']
                Appro.totalpro_rev=request.POST['totalpro_rev']
                

                Appro.pen_occ1=request.POST['pen_occ1']
                Appro.pen_adr1=request.POST['pen_adr1']
                Appro.pen_rev1=request.POST['pen_rev1']
                Appro.pen_occ2=request.POST['pen_occ2']
                Appro.pen_adr2=request.POST['pen_adr2']
                Appro.pen_rev2=request.POST['pen_rev2']
                Appro.pen_occ3=request.POST['pen_occ3']
                Appro.pen_adr3=request.POST['pen_adr3']
                Appro.pen_rev3=request.POST['pen_rev3']
                Appro.totalpen_occ=request.POST['totalpen_occ']
                Appro.totalpen_adr=request.POST['totalpen_adr']
                Appro.totalpen_rev=request.POST['totalpen_rev']
                Appro.ModifyBy=UserID
                Appro.save()
                return redirect('Project_list')
        else:
                Hotel_type = request.POST['Hotel_type']
                Strategy=request.POST['Strategy']
                Development_type=request.POST['Development_type']
                Status=request.POST['Status']
                Opening_Date=request.POST['Opening_Date']
                RHG_Contribution=request.POST['RHG_Contribution']
                Fee_income=request.POST['Fee_income']
                IRR_applicable=request.POST['IRR_applicable']
            
                Location=request.POST['Location']
                Location_label=request.POST['Location_label']
                Location_type=request.POST['Location_type']
                Rooms=request.POST['Rooms']
                FB_outlets=request.POST['FB_outlets']
                MeetingCoWork=request.POST['MeetingCoWork']
                Other=request.POST['Other']
               
                adr_fv=request.POST['adr_fv']
                adr_pv=request.POST['adr_pv']
                occ=request.POST['occ']
                rav_fv=request.POST['rav_fv']
                rev_pv=request.POST['rev_pv']
                rrev=request.POST['rrev']
                term=request.POST['term']
                in_rate=request.POST['in_rate']
                royalty_fee1=request.POST['royalty_fee1']
                royalty_fee2=request.POST['royalty_fee2']
                zma_fee1=request.POST['zma_fee1']
                zma_fee2=request.POST['zma_fee2']
                total_fee1=request.POST['total_fee1']
                total_fee2=request.POST['total_fee2']
                total_fee3=request.POST['total_fee3']
                meur=request.POST['meur']
                yp1=request.POST['yp1']
                yp2=request.POST['yp2']

                year1=request.POST['year1']
                year2=request.POST['year2']
                year3=request.POST['year3']
                occ1=request.POST['occ1']
                rc1=request.POST['rc1']
                old_rev1=request.POST['old_rev1']
                occ2=request.POST['occ2']
                rc2=request.POST['rc2']
                old_rev2=request.POST['old_rev2']
                occ3=request.POST['occ3']
                rc3=request.POST['rc3']
                old_rev3=request.POST['old_rev3']
                totalocc=request.POST['totalocc']
                totalrc=request.POST['totalrc']
                total_rev=request.POST['total_rev']

                com_occ1=request.POST['com_occ1']
                com_adr1=request.POST['com_adr1']
                com_rev1=request.POST['com_rev1']
                com_occ2=request.POST['com_occ2']
                com_adr2=request.POST['com_adr2']
                com_rev2=request.POST['com_rev2']
                com_occ3=request.POST['com_occ3']
                com_adr3=request.POST['com_adr3']
                com_rev3=request.POST['com_rev3']
                totalcom_occ=request.POST['totalcom_occ']
                totalcom_adr=request.POST['totalcom_adr']
                totalcom_rev=request.POST['totalcom_rev']
                
                pro_occ1=request.POST['pro_occ1']
                pro_adr1=request.POST['pro_adr1']
                pro_rev1=request.POST['pro_rev1']
                pro_occ2=request.POST['pro_occ2']
                pro_adr2=request.POST['pro_adr2']
                pro_rev2=request.POST['pro_rev2']
                pro_occ3=request.POST['pro_occ3']
                pro_adr3=request.POST['pro_adr3']
                pro_rev3=request.POST['pro_rev3']
                total_pro_occ=request.POST['total_pro_occ']
                totalpro_adr=request.POST['totalpro_adr']
                totalpro_rev=request.POST['totalpro_rev']
                

                pen_occ1=request.POST['pen_occ1']
                pen_adr1=request.POST['pen_adr1']
                pen_rev1=request.POST['pen_rev1']
                pen_occ2=request.POST['pen_occ2']
                pen_adr2=request.POST['pen_adr2']
                pen_rev2=request.POST['pen_rev2']
                pen_occ3=request.POST['pen_occ3']
                pen_adr3=request.POST['pen_adr3']
                pen_rev3=request.POST['pen_rev3']
                totalpen_occ=request.POST['totalpen_occ']
                totalpen_adr=request.POST['totalpen_adr']
                totalpen_rev=request.POST['totalpen_rev']
                
                approvel = Project_Approvel_Request.objects.create(Hotel_type=Hotel_type,Strategy=Strategy,Development_type=Development_type,Status=Status,
                                                                Opening_Date=Opening_Date,RHG_Contribution=RHG_Contribution,Fee_income=Fee_income,
                                                                IRR_applicable=IRR_applicable,Location=Location,Location_label=Location_label,
                                                                Location_type=Location_type,Rooms=Rooms,FB_outlets=FB_outlets,MeetingCoWork=MeetingCoWork,
                                                                Other=Other,adr_fv=adr_fv,adr_pv=adr_pv,occ=occ,rav_fv=rav_fv,rev_pv=rev_pv,
                                                                rrev=rrev,term=term,in_rate=in_rate,royalty_fee1=royalty_fee1,royalty_fee2=royalty_fee2
                                                                ,zma_fee1=zma_fee1,zma_fee2=zma_fee2,total_fee1=total_fee1,total_fee2=total_fee2,
                                                                total_fee3=total_fee3,meur=meur,yp1=yp1,yp2=yp2,year1=year1,year2=year2,year3=year3,occ1=occ1,rc1=rc1,old_rev1=old_rev1,
                                                                occ2=occ2,rc2=rc2,old_rev2=old_rev2,occ3=occ3,rc3=rc3,old_rev3=old_rev3,totalocc=totalocc,totalrc=totalrc,total_rev=total_rev, 
                                                               com_occ1=com_occ1,com_adr1=com_adr1,com_rev1=com_rev1,com_occ2=com_occ2,com_adr2=com_adr2,com_rev2=com_rev2,
                                                                 com_occ3=com_occ3,com_adr3=com_adr3,com_rev3=com_rev3,totalcom_occ=totalcom_occ,totalcom_adr=totalcom_adr,totalcom_rev=totalcom_rev,
                                                                 pro_occ1=pro_occ1,pro_adr1=pro_adr1,pro_rev1=pro_rev1,pro_occ2=pro_occ2,pro_adr2=pro_adr2,pro_rev2=pro_rev2,
                                                                 pro_occ3=pro_occ3,pro_adr3=pro_adr3,pro_rev3=pro_rev3,total_pro_occ=total_pro_occ,totalpro_adr=totalpro_adr,totalpro_rev=totalpro_rev,
                                                                 pen_occ1=pen_occ1,pen_adr1=pen_adr1,pen_rev1=pen_rev1,pen_occ2=pen_occ2,pen_adr2=pen_adr2,pen_rev2=pen_rev2,pen_occ3=pen_occ3,
                                                                 pen_adr3=pen_adr3,pen_rev3=pen_rev3,totalpen_occ=totalpen_occ,totalpen_adr=totalpen_adr,totalpen_rev=totalpen_rev,OrganizationID=OrganizationID,CreatedBy=UserID)










                ContractTotal = int(request.POST["ContractTotal"])
                for i in range(ContractTotal + 1):
                    Con_key = "Contract_ID_" + str(i)
                    Con_value = request.POST.get(Con_key)
                    Cons = Contract_summary.objects.get(id=Con_value)
                    Deta__key = "Deta_" + str(i) 
                    Deta__value = request.POST.get(Deta__key) or 0
                    
                    
                    squer = Contract_deta.objects.create(
                                                   Contract_summary=Cons,Project_Approvel_Request=approvel,Deta=Deta__value,OrganizationID=OrganizationID,CreatedBy=UserID )
                    

                OwnerTotal = int(request.POST["OwnerTotal"])
                for i in range(OwnerTotal + 1):
                    ow_key = "ownes_ID_" + str(i)
                    ow_value = request.POST.get(ow_key)
                    owners_details = owners.objects.get(id=ow_value)
                    Deta2__key = "Deta2_" + str(i) 
                    Deta2__value = request.POST.get(Deta2__key) or 0
                    
                    
                    ow = owner_deta.objects.create(
                                                   owners=owners_details,Project_Approvel_Request=approvel,Deta2=Deta2__value,OrganizationID=OrganizationID,CreatedBy=UserID )    
                                                            
                ProjectTotal = int(request.POST["ProjectTotal"])
                for i in range(ProjectTotal + 1):
                    p_key = "project_ID_" + str(i)
                    p_value = request.POST.get(p_key)
                    project_details = Project.objects.get(id=p_value)
                    Deta3__key = "Deta3_" + str(i) 
                    Deta3__value = request.POST.get(Deta3__key) or 0
                    
                    
                    ow = project_deta.objects.create(
                                                   Project=project_details,Project_Approvel_Request=approvel,Deta3=Deta3__value,OrganizationID=OrganizationID,CreatedBy=UserID )    
                
             
                  
                return redirect('Project_list')
        
    context={'Appro':Appro,'Contract':Contract,'ownes':ownes,'project':project,'Oppo':Oppo}
    return render(request,'Approvel/Project_add.html',context)
    
    
    
    
    
    
    
    
    
    


def Project_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    


    
    aprovellist = Project_Approvel_Request.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    
    
    context={'aprovellist':aprovellist}
    
    return render(request,'Approvel/Project_list.html',context)



def project_delete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    app=Project_Approvel_Request.objects.get(id=id)
    app.IsDelete=True
    app.ModifyBy=UserID
    app.save()
    return redirect('Project_list')






from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import uuid
from datetime import datetime


def pdf(request):
    id = request.GET.get('ID')
    if id is None:
        return HttpResponse("ID parameter is missing.")
    
    try:
        approvels = Project_Approvel_Request.objects.get(id=id)
    except Project_Approvel_Request.DoesNotExist:
        return HttpResponse("Project review with provided ID does not exist.")
    
    OrganizationID = request.session.get("OrganizationID")
    
            

    
   
   
    opportunity = Opportunityss.objects.filter(IsDelete=False,OrganizationID=OrganizationID)

    Contract = Contract_summary.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    deta = Contract_deta.objects.filter(Project_Approvel_Request=approvels,IsDelete=False,OrganizationID=OrganizationID)

    ownes = owners.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    ow_deta = owner_deta.objects.filter(Project_Approvel_Request=approvels,IsDelete=False,OrganizationID=OrganizationID)

    project = Project.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    pro_deta = project_deta.objects.filter(Project_Approvel_Request=approvels,IsDelete=False,OrganizationID=OrganizationID)






    template_path = 'Approvel/pdf.html'
    context = {'approvels': approvels,'opportunity':opportunity,'Contract':Contract,'ownes':ownes,'project':project,'deta':deta,'ow_deta':ow_deta,'pro_deta':pro_deta}
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Project_Approval_request.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    
    pisa_status = pisa.CreatePDF(html, dest=response)
   
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
     