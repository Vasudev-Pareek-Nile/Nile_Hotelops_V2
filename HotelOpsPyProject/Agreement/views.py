from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import  Master_title,Master_subartical,Master_childartical,agreement,uplodede,update_expired_agreements,Master_subchildartical
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

# Create your views here.
def agreement_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    add_id=request.GET.get('ID')
    add = None
    if add_id is not None:
            add = get_object_or_404(agreement,id=add_id,OrganizationID=OrganizationID)
    if request.method == "POST":
        if add_id is not None:
            add.company_name = request.POST['company_name']
            add.address = request.POST['address']
            add.pan_number = request.POST['pan_number']
            add.Director_Name = request.POST['Director_Name']
            add.Near_Location = request.POST['Near_Location']
            add.Name_of_Hotel = request.POST['Name_of_Hotel']
            add.Number_of_Room = request.POST['Number_of_Room']
            add.Years = request.POST['Years']
            add.percentage = request.POST['percentage']
            add.sum_of_inr=request.POST['sum_of_inr']
            add.license_fee=request.POST['license_fee']
            add.Management_Services_N_N=request.POST['Management_Services_N_N']
            add.Owner_Attention=request.POST['Owner_Attention']
            add.Owner_Address=request.POST['Owner_Address']
            add.Owner_Tel_No=request.POST['Owner_Tel_No']
            add.Owner_Fax_No=request.POST['Owner_Fax_No']
            add.Owner_Email_Id=request.POST['Owner_Email_Id']
            add.Operator_Attention=request.POST['Operator_Attention']
            add.Operator_Address=request.POST['Operator_Address']
            add.Operator_Tel_No=request.POST['Operator_Tel_No']
            add.Operator_Fax_No=request.POST['Operator_Fax_No']
            add.Operator_Email_Id=request.POST['Operator_Email_Id']
            add.Authorized_Director=request.POST['Authorized_Director']
            add.Name_Witness1=request.POST['Name_Witness1']
            add.Name_Witness2=request.POST['Name_Witness2']
            add.start_date=request.POST['start_date']
            add.end_date=request.POST['end_date']
            
            add.ModifyBy =UserID
            add.save()
        else:

            company_name = request.POST['company_name']
            address = request.POST['address']
            pan_number = request.POST['pan_number']
            Director_Name = request.POST['Director_Name']
            Near_Location = request.POST['Near_Location']
            Name_of_Hotel = request.POST['Name_of_Hotel']
            Number_of_Room = request.POST['Number_of_Room']
            Years = request.POST['Years']
            percentage = request.POST['percentage']
            sum_of_inr = request.POST['sum_of_inr']
            license_fee = request.POST['license_fee']
            Management_Services_N_N = request.POST['Management_Services_N_N']
            Owner_Attention=request.POST['Owner_Attention']
            Owner_Address=request.POST['Owner_Address']
            Owner_Tel_No=request.POST['Owner_Tel_No']
            Owner_Fax_No=request.POST['Owner_Fax_No']
            Owner_Email_Id=request.POST['Owner_Email_Id']
            Operator_Attention=request.POST['Operator_Attention']
            Operator_Address=request.POST['Operator_Address']
            Operator_Tel_No=request.POST['Operator_Tel_No']
            Operator_Fax_No=request.POST['Operator_Fax_No']
            Operator_Email_Id=request.POST['Operator_Email_Id']
            Authorized_Director=request.POST['Authorized_Director']
            Name_Witness1=request.POST['Name_Witness1']
            Name_Witness2=request.POST['Name_Witness2']
            start_date=request.POST['start_date']
            end_date=request.POST['end_date']
            
            

            agreementmodel=agreement.objects.create(company_name=company_name,address=address,pan_number=pan_number,Director_Name=Director_Name,
                                                Near_Location=Near_Location,Name_of_Hotel=Name_of_Hotel,Number_of_Room=Number_of_Room,
                                                    Years=Years,percentage=percentage,sum_of_inr=sum_of_inr,
                                                   license_fee=license_fee,Management_Services_N_N=Management_Services_N_N,Owner_Attention=Owner_Attention,Owner_Address=Owner_Address,
                                                   Owner_Tel_No=Owner_Tel_No,Owner_Fax_No=Owner_Fax_No,Owner_Email_Id=Owner_Email_Id,Operator_Attention=Operator_Attention,
                                                   Operator_Address=Operator_Address,Operator_Tel_No=Operator_Tel_No,Operator_Fax_No=Operator_Fax_No,
                                                   Operator_Email_Id=Operator_Email_Id,Authorized_Director=Authorized_Director,Name_Witness1=Name_Witness1,
                                                   Name_Witness2=Name_Witness2,start_date=start_date,end_date=end_date,
                                                   OrganizationID=OrganizationID,CreatedBy=UserID,)

           

        return redirect('agreement_list')
    context={'add':add}    
    return render(request,'agreement/agreement_add.html',context)


def agreement_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    addlist = agreement.objects.filter(IsDelete=False, OrganizationID=OrganizationID).order_by('-id')  

    total_contracts = addlist.filter(IsDelete=False).count()

    generated_count = addlist.filter(status=0).count()
    signed_count = addlist.filter(status=1).count()

    
    now = datetime.now()

    
    exp =update_expired_agreements()
    expired_count = addlist.filter(status=-1).count()
    context = {
        'addlist': addlist,
        'total_contracts': total_contracts,
        'generated_count': generated_count,
        'signed_count': signed_count,
        'expired_count': expired_count,
    }

    for contract in addlist:
        if contract.status == 1 and contract.end_date < now.date():
            contract.status_text = 'Expired'
        else:
            contract.status_text = 'Signed' if contract.status == 1 else 'Generated'

    return render(request, 'agreement/agreement_list.html', context)


def agreement_delet(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    agreementdelet=agreement.objects.get(id=id)
    agreementdelet.IsDelete=True
    agreementdelet.ModifyBy=UserID
    agreementdelet.save()
    return redirect('agreement_list')









def master_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    masterlists = Master_title.objects.filter(IsDelete=False,OrganizationID=OrganizationID)  
    context={'masterlists':masterlists}
    

    return render(request,'agreement/master_list.html',context)



def master_add(request):
            
            if 'OrganizationID' not in request.session:
                return redirect(MasterAttribute.Host)
            else:
                print("Show Page Session")
        
        
            OrganizationID =request.session["OrganizationID"]
            UserID =str(request.session["UserID"])
            agreemnt_id=request.GET.get('ID')
            agreemnt=None
            if agreemnt_id is not None:
                agreemnt = get_object_or_404(Master_title,id=agreemnt_id,OrganizationID=OrganizationID)
            if request.method=="POST":
                if agreemnt_id is not None: 
                        agreemnt.artical_number = request.POST['artical_number']
                        agreemnt.name_artical = request.POST['name_artical']
                        agreemnt.ModifyBy =UserID
                        agreemnt.save()   
                else:
                    artical_number = request.POST['artical_number']
                    name_artical = request.POST['name_artical']
                    masteradd =Master_title.objects.create(artical_number=artical_number,name_artical=name_artical,OrganizationID=OrganizationID,CreatedBy=UserID,)
                return redirect('master_list') 
                    

                
            context ={'agreemnt':agreemnt}   
            return render(request,'agreement/master_add.html',context)


def master_delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
  
   
     OrganizationID =request.session["OrganizationID"]
     UserID =str(request.session["UserID"])
     
     id=request.GET.get('ID')
     masteradd=Master_title.objects.get(id=id)
     masteradd.IsDelete=True
     masteradd.ModifyBy=UserID
     masteradd.save()
     return redirect('master_list')


# Sub article master add urls



def sub_articlelist(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    Sublists = Master_subartical.objects.filter(Master_title_id=id,IsDelete=False,OrganizationID=OrganizationID)  
    context={'Sublists':Sublists,'id':id,}
    

    return render(request, 'agreement/sub_articlelist.html',context)


def sub_articleadd(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    id=request.GET.get('ID')
    Master_title_instancemtn = Master_title.objects.get(id=id,IsDelete=False)
    mtn= Master_title_instancemtn.artical_number
    m_id=request.GET.get('M_ID')
    m_sub=None
    if m_id is not None:
         m_sub=Master_subartical.objects.get(id=m_id,IsDelete=False)

    if request.method == "POST":
        if m_id is not None:
             m_sub.subartical_number = request.POST['subartical_number']
             m_sub.sub_artical = request.POST['sub_artical']
             m_sub.ModifyBy = UserID
             m_sub.save()
             
        else: 
        
            subartical_number = request.POST['subartical_number']
            sub_artical = request.POST['sub_artical']
            
            
            
            subarticaladd = Master_subartical.objects.create(
                
                subartical_number=subartical_number,
                sub_artical=sub_artical,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
                Master_title=Master_title_instancemtn
            )
        return redirect('/Agreement/sub_articlelist/?ID='+str(id)) 
    context ={'mtn':mtn,'m_sub':m_sub}   

    return render(request, 'agreement/sub_articleadd.html',context)


def sub_delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
  
   
     OrganizationID =request.session["OrganizationID"]
     UserID =str(request.session["UserID"])
     
     
     id=request.GET.get('ID')
     subadd=Master_subartical.objects.get(id=id)
     subadd.IsDelete=True
     subadd.ModifyBy=UserID
     subadd.save()
     return redirect('sub_articlelist')



def child_articlelist(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
  
   
     OrganizationID =request.session["OrganizationID"]
     UserID =str(request.session["UserID"])
     c_id=request.GET.get('ID')
     childlists = Master_childartical.objects.filter(Master_subartical_id=c_id,IsDelete=False,OrganizationID=OrganizationID)  
     context={'childlists':childlists,'c_id':c_id,}
     return render(request, 'agreement/child_articlelist.html',context)


def Child_articleadd(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    Master_subartical_instancemtnc = Master_subartical.objects.get(id=id,IsDelete=False)
    mtnc= Master_subartical_instancemtnc.subartical_number
    mtn = Master_subartical_instancemtnc.Master_title.artical_number
    ct_id=request.GET.get("CT_ID")
    ct_sub = None
    if ct_id is not None:
         ct_sub = Master_childartical.objects.get(id=ct_id,IsDelete=False)

    if request.method=="POST":
        if ct_id is not None: 
            ct_sub.childartical_number= request.POST['childartical_number']
            ct_sub.child_artical= request.POST['child_artical']
            ct_sub.ModifyBy = UserID
            ct_sub.save()
            
        else :
            childartical_number= request.POST['childartical_number']
            child_artical= request.POST['child_artical']
            childadd=Master_childartical.objects.create(childartical_number=childartical_number,
                                                        child_artical=child_artical,OrganizationID=OrganizationID,
                                                        CreatedBy=UserID,
                                                        Master_subartical=Master_subartical_instancemtnc,)
        return redirect('/Agreement/child_articlelist/?ID='+str(id))
    context ={'mtnc':mtnc,'mtn':mtn, 'ct_sub':ct_sub,}
   
    return render(request, 'agreement/Child_articleadd.html',context)



def child_delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
  
   
     OrganizationID =request.session["OrganizationID"]
     UserID =str(request.session["UserID"])
     
     id=request.GET.get('ID')
     childadd=Master_childartical.objects.get(id=id)
     childadd.IsDelete=True
     childadd.ModifyBy=UserID
     childadd.save()
     return redirect('child_articlelist')
      



def view_agreement(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
    
    
     OrganizationID =request.session["OrganizationID"]
     UserID =str(request.session["UserID"])
     masterlists = Master_title.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
     Sublists = Master_subartical.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
     childlists = Master_childartical.objects.filter(IsDelete=False,OrganizationID=OrganizationID) 
     context ={'masterlists':masterlists,'Sublists':Sublists, 'childlists':childlists,}
     
     return render(request,'agreement/view_agreement.html',context)      



from django.http import HttpResponse
from io import BytesIO    
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template.loader import render_to_string

def agreement_pdf(request):
        
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    id = request.GET.get('ID')
    agreementlist = get_object_or_404(agreement, id=id)
     
    template_path = "agreement/agreement_pdf.html"
        
    masterlists = Master_title.objects.filter(IsDelete=False, OrganizationID=OrganizationID)
    Sublists = Master_subartical.objects.filter(IsDelete=False, OrganizationID=OrganizationID)
    childlists = Master_childartical.objects.filter(IsDelete=False, OrganizationID=OrganizationID) 
    subchild_lists = Master_subchildartical.objects.filter(IsDelete=False, OrganizationID=OrganizationID)

   
    
       

    for childlist in childlists:
        replaced_text = childlist.child_artical.replace("&&NoRoom&&", f"**{agreementlist.Number_of_Room}**")
        childlist.child_artical = replaced_text
     
     

    for subchild in subchild_lists:
        subchild.childsub_artical = subchild.childsub_artical.replace("&&ownerattions&&",agreementlist.Owner_Attention)     
        subchild.childsub_artical = subchild.childsub_artical.replace("&&Address123&&",agreementlist.Owner_Address)
        subchild.childsub_artical = subchild.childsub_artical.replace("&&ownerTel&&",agreementlist.Owner_Tel_No)
        subchild.childsub_artical = subchild.childsub_artical.replace("&&ownerFax&&",agreementlist.Owner_Fax_No)
        subchild.childsub_artical = subchild.childsub_artical.replace("&&ownergmail&&",agreementlist.Owner_Email_Id)
        subchild.childsub_artical = subchild.childsub_artical.replace("&&Operatorattion&&",agreementlist.Operator_Attention) 
        subchild.childsub_artical = subchild.childsub_artical.replace("&&Operatoraaddrees&&",agreementlist.Operator_Address)
        subchild.childsub_artical = subchild.childsub_artical.replace("&&Operatorrtel&&",agreementlist.Operator_Tel_No)
        subchild.childsub_artical = subchild.childsub_artical.replace("&&Operatorfax&&",agreementlist.Operator_Fax_No)
        subchild.childsub_artical = subchild.childsub_artical.replace("&&Operatorgmail&&",agreementlist.Operator_Email_Id)
   
                                 
    ga=1; 
    
    for m in masterlists:
        m.LoopIndex = ga
        si=1  
        sl = Master_subartical.objects.filter(IsDelete=False,Master_title=m.id)
        
        for sli in sl:
            for Sublist in sl:
                print(Sublist.sub_artical)
                if Sublist.sub_artical is not None and "&&years&&" in Sublist.sub_artical:
                    Sublist.sub_artical = Sublist.sub_artical.replace("&&years&&", agreementlist.Years)

                if Sublist.sub_artical is not None and "&&parsent&&" in Sublist.sub_artical:
                    Sublist.sub_artical = Sublist.sub_artical.replace("&&parsent&&", agreementlist.percentage)

                if Sublist.sub_artical is not None and "&&Lakhs&&" in Sublist.sub_artical:
                    Sublist.sub_artical = Sublist.sub_artical.replace("&&Lakhs&&", agreementlist.sum_of_inr)

                if Sublist.sub_artical is not None and "&&licensefee&&" in Sublist.sub_artical:
                    Sublist.sub_artical = Sublist.sub_artical.replace("&&licensefee&&", agreementlist.license_fee)

                if Sublist.sub_artical is not None and "&&NoRoom&&" in Sublist.sub_artical:
                    Sublist.sub_artical = Sublist.sub_artical.replace("&&NoRoom&&", agreementlist.Number_of_Room)

            sli.LoopIndex=si
           
            si=si+1
        m.sublist = sl
        ga=ga+1
        
    
    mydict = {
        'masterlists': masterlists,
        'Sublists': Sublists, 
        'childlists': childlists,
        'subchild_lists':subchild_lists,

        'agreementlist': agreementlist
    }
   
    
    html_content = render_to_string(template_path, mydict, request=request)
    
    
    
    html_content_with_overline = html_content.replace(
        "Text to Overline", 
        '<span style="text-decoration: overline;">Text to Overline</span>'
    )
        
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content_with_overline.encode("UTF-8")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None






def agreement_uploded(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    id = request.GET.get('ID')
    agreementN = agreement.objects.get(IsDelete=False, OrganizationID=OrganizationID, id=id)
    
    if request.method == "POST":
        pdf_filenn = request.FILES.get('pdf_filenn')
        if pdf_filenn:
            
            uplodede_instance = uplodede.objects.create(pdf_filenn=pdf_filenn, agreement=agreementN)
            
            agreementN.status = 1
            agreementN.save()
            messages.success(request, 'PDF uploaded successfully.')
            return redirect('agreement_list')
        else:
            messages.error(request, 'No PDF file uploaded.')
    
    return render(request, 'agreement/agreement_uploded.html')




def subchild(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    Master_childartical_instancemtnc = Master_childartical.objects.get(id=id,IsDelete=False)
    
    mtnm = Master_childartical_instancemtnc.childartical_number
    sct_id=request.GET.get("CT_ID")
    sct_sub = None
    if sct_id is not None:
         sct_sub = Master_childartical.objects.get(id=sct_id,IsDelete=False)

    if request.method=="POST":
        if sct_id is not None: 
            sct_sub.childsubartical_number= request.POST['childsubartical_number']
            sct_sub.childsub_artical= request.POST['childsub_artical']
            sct_sub.ModifyBy = UserID
            sct_sub.save()
            
        else :
            childsubartical_number= request.POST['childsubartical_number']
            childsub_artical= request.POST['childsub_artical']
            childadd=Master_subchildartical.objects.create(childsubartical_number=childsubartical_number,
                                                        childsub_artical=childsub_artical,OrganizationID=OrganizationID,
                                                        CreatedBy=UserID,
                                                        Master_childartical=Master_childartical_instancemtnc,)
        return redirect('/Agreement/subchild_list/?ID='+str(id))
    context ={'mtnm':mtnm, 'sct_sub':sct_sub,}
    return render(request, 'agreement/subchild.html',context)



















def subchild_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    sc_id = request.GET.get('ID')

    
    master_child = Master_childartical.objects.get(id=sc_id)

    
    subchild_lists = Master_subchildartical.objects.filter(
        Master_childartical=master_child,
        IsDelete=False,
        OrganizationID=OrganizationID
    )

    print(subchild_lists)

    context = {
        'subchild_lists': subchild_lists,
        'sc_id': sc_id,
    }

    return render(request, 'agreement/subchild_list.html', context)


def subchild_delet(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
        
    id=request.GET.get('ID')
    subchild=Master_subchildartical.objects.get(id=id)
    subchild.IsDelete=True
    subchild.ModifyBy=UserID
    subchild.save()
    return redirect('/Agreement/subchild_list/?ID='+str(id)) 
