def PADP_View(request):
        if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
        else:
            print("Show Page Session")
        OrganizationID = request.session["OrganizationID"]
        
        UserID = str(request.session["UserID"]) 
        
        objs =  Objective_Master.objects.filter(IsDelete=False)
        for m in objs:
            attr1= Attribute_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Attibutes = attr1
            Effect1 = Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Effectives = Effect1
            Infect1 = Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Ineffectives = Infect1
        padp_id = request.GET.get('ID')
        padp =None
        sum_data = None
        if padp_id is not None:
            padp = Entry_Master.objects.filter(IsDelete =False,id = padp_id).first()
            Leadership_Detail = Leadership_Details.objects.filter(Entry_Master=padp
                                                ,IsDelete =False)
            sum_data = SUMMARY_AND_ACKNOWLEDGEMENT.objects.filter(Entry_Master=padp
                                                ,IsDelete =False).first()
            
            
            for m in objs:
                
                m.LD= Leadership_Details.objects.filter(Entry_Master=padp,Objective_Master=m,
                                                IsDelete =False)
                
                m.SP_MEAS_ACHI = SPECIFIC_MEASURABLE_ACHIEVABLE.objects.filter(Entry_Master=padp,Objective_Master=m
                                                ,IsDelete =False)
                
                m.SPE_MEA_ACH_Detail = SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.filter(SPECIFIC_MEASURABLE_ACHIEVABLE__Objective_Master=m,SPECIFIC_MEASURABLE_ACHIEVABLE__Entry_Master = padp,IsDelete =False)  
                
                

                
                attr1= Attribute_Master.objects.filter(IsDelete=False,Objective_Master=m)
                m.Attibutes = attr1
                for a in attr1:
                        k = Leadership_AttributeDetails.objects.filter(
                                                IsDelete =False,Leadership_Details__Objective_Master=m,Attribute_Master=a,Leadership_Details__Entry_Master = padp)
                        
                        a.detailatt = k

                Effect1 = Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
                m.Effectives = Effect1
                for eff in  Effect1:
                    c = Effective_Indicators_Details_Appraisee.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff,)
                
                    eff.effdetail_Appee = c
                
                    d = Effective_Indicators_Details_Appraisor.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff)
                    eff.effdetail_Appor = d 
                Infect1 = Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
                m.Ineffectives = Infect1
                for inff in Infect1:
                    kl = Ineffective_Indicators_Details_Appraisee.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff
                    )    
                    inff.inffdetailAppee =  kl
                    ml = Ineffective_Indicators_Details_Appraisor.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff
                    )    
                    inff.inffdetailAppor =  ml   
    
        template_path = "PADPAPP/PADP/PADPVIEW.html"
        # NileLogo=MasterAttribute.NileLogo
        
        mydict={'objs':objs,'padp':padp,'sum_data':sum_data}
        #  ScantyBaggageForm=forms.ScantyBaggageForm()
        
        
        

        # context = {'myvar': 'this is your template context','p':varM}
        
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="padp.pdf"'
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



