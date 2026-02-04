from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.
class Project_Approvel_Request(models.Model):
    Hotel_type=models.CharField(max_length=250, blank=True ,null=True)
    Strategy=models.CharField(max_length=250, blank=True ,null=True)
    Development_type=models.CharField(max_length=250, blank=True ,null=True)
    Status=models.CharField(max_length=250, blank=True ,null=True)
    Opening_Date=models.DateTimeField(default=timezone.now)
    RHG_Contribution=models.CharField(max_length=250, blank=True ,null=True)
    Fee_income=models.CharField(max_length=250, blank=True ,null=True)
    IRR_applicable=models.CharField(max_length=250, blank=True ,null=True)
    
   
    
    Location=models.CharField(max_length=250, blank=True ,null=True)
    Location_label=models.CharField(max_length=250, blank=True ,null=True)
    Location_type=models.CharField(max_length=250, blank=True ,null=True)
    Rooms=models.CharField(max_length=250, blank=True ,null=True)
    FB_outlets=models.CharField(max_length=250, blank=True ,null=True)
    MeetingCoWork=models.CharField(max_length=250, blank=True ,null=True)
    Other=models.CharField(max_length=250, blank=True ,null=True)
    
    adr_fv=models.CharField(max_length=250, blank=True ,null=True)
    adr_pv=models.CharField(max_length=250, blank=True ,null=True)
    occ=models.CharField(max_length=250, blank=True ,null=True)
    rav_fv=models.CharField(max_length=250, blank=True ,null=True)
    rev_pv=models.CharField(max_length=250, blank=True ,null=True)
    rrev=models.CharField(max_length=250, blank=True ,null=True)
    term=models.CharField(max_length=250, blank=True ,null=True)
    in_rate=models.CharField(max_length=250, blank=True ,null=True)

    royalty_fee1=models.CharField(max_length=250, blank=True ,null=True)
    royalty_fee2=models.CharField(max_length=250, blank=True ,null=True)
    zma_fee1=models.CharField(max_length=250, blank=True ,null=True)
    zma_fee2=models.CharField(max_length=250, blank=True ,null=True)
    total_fee1=models.CharField(max_length=250, blank=True ,null=True)
    total_fee2=models.CharField(max_length=250, blank=True ,null=True)
    total_fee3=models.CharField(max_length=250, blank=True ,null=True)
    meur=models.CharField(max_length=250, blank=True ,null=True)
    yp1=models.CharField(max_length=250, blank=True ,null=True)
    yp2=models.CharField(max_length=250, blank=True ,null=True)

    year1=models.CharField(max_length=250, blank=True ,null=True)
    year2=models.CharField(max_length=250, blank=True ,null=True)
    year3=models.CharField(max_length=250, blank=True ,null=True)




    occ1=models.CharField(max_length=250, blank=True ,null=True)
    rc1=models.CharField(max_length=250, blank=True ,null=True)
    old_rev1=models.CharField(max_length=250, blank=True ,null=True)
    occ2=models.CharField(max_length=250, blank=True ,null=True)
    rc2=models.CharField(max_length=250, blank=True ,null=True)
    old_rev2=models.CharField(max_length=250, blank=True ,null=True)
    occ3=models.CharField(max_length=250, blank=True ,null=True)
    rc3=models.CharField(max_length=250, blank=True ,null=True)
    old_rev3=models.CharField(max_length=250, blank=True ,null=True)
    totalocc=models.CharField(max_length=250, blank=True ,null=True)
    totalrc=models.CharField(max_length=250, blank=True ,null=True)
    total_rev=models.CharField(max_length=250, blank=True ,null=True)


    com_occ1=models.CharField(max_length=250, blank=True ,null=True)
    com_adr1=models.CharField(max_length=250, blank=True ,null=True)
    com_rev1=models.CharField(max_length=250, blank=True ,null=True)
    com_occ2=models.CharField(max_length=250, blank=True ,null=True)
    com_adr2=models.CharField(max_length=250, blank=True ,null=True)
    com_rev2=models.CharField(max_length=250, blank=True ,null=True)
    com_occ3=models.CharField(max_length=250, blank=True ,null=True)
    com_adr3=models.CharField(max_length=250, blank=True ,null=True)
    com_rev3=models.CharField(max_length=250, blank=True ,null=True)
    totalcom_occ=models.CharField(max_length=250, blank=True ,null=True)
    totalcom_adr=models.CharField(max_length=250, blank=True ,null=True)
    totalcom_rev=models.CharField(max_length=250, blank=True ,null=True)

    pro_occ1=models.CharField(max_length=250, blank=True ,null=True)
    pro_adr1=models.CharField(max_length=250, blank=True ,null=True)
    pro_rev1=models.CharField(max_length=250, blank=True ,null=True)
    pro_occ2=models.CharField(max_length=250, blank=True ,null=True)
    pro_adr2=models.CharField(max_length=250, blank=True ,null=True)
    pro_rev2=models.CharField(max_length=250, blank=True ,null=True)
    pro_occ3=models.CharField(max_length=250, blank=True ,null=True)
    pro_adr3=models.CharField(max_length=250, blank=True ,null=True)
    pro_rev3=models.CharField(max_length=250, blank=True ,null=True)
    total_pro_occ=models.CharField(max_length=250, blank=True ,null=True)
    totalpro_adr=models.CharField(max_length=250, blank=True ,null=True)
    totalpro_rev=models.CharField(max_length=250, blank=True ,null=True)

    pen_occ1=models.CharField(max_length=250, blank=True ,null=True)
    pen_adr1=models.CharField(max_length=250, blank=True ,null=True)
    pen_rev1=models.CharField(max_length=250, blank=True ,null=True)
    pen_occ2=models.CharField(max_length=250, blank=True ,null=True)
    pen_adr2=models.CharField(max_length=250, blank=True ,null=True)
    pen_rev2=models.CharField(max_length=250, blank=True ,null=True)
    pen_occ3=models.CharField(max_length=250, blank=True ,null=True)
    pen_adr3=models.CharField(max_length=250, blank=True ,null=True)
    pen_rev3=models.CharField(max_length=250, blank=True ,null=True)
    totalpen_occ=models.CharField(max_length=250, blank=True ,null=True)
    totalpen_adr=models.CharField(max_length=250, blank=True ,null=True)
    totalpen_rev=models.CharField(max_length=250, blank=True ,null=True)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default = False)
    def __str__(self):
         return self.Hotel_type 













    



class Opportunityss(models.Model):
        oppor= models.TextField()
        OrganizationID = models.BigIntegerField(default=0)
        CreatedBy = models.BigIntegerField(default=0)
        CreatedDateTime = models.DateTimeField(default=timezone.now)
        ModifyBy = models.BigIntegerField(default=0)
        ModifyDateTime = models.DateTimeField(default=timezone.now)
        IsDelete = models.BooleanField(default = False)
        def __str__(self):
            return self.oppor 
        
        






    




class Contract_summary(models.Model):
        Name=models.CharField(max_length=250, blank=True ,null=True)
        OrganizationID = models.BigIntegerField(default=0)
        CreatedBy = models.BigIntegerField(default=0)
        CreatedDateTime = models.DateTimeField(default=timezone.now)
        ModifyBy = models.BigIntegerField(default=0)
        ModifyDateTime = models.DateTimeField(default=timezone.now)
        IsDelete = models.BooleanField(default = False)
        def __str__(self):
            return self.Name 
        

class owners(models.Model):
        Name1=models.CharField(max_length=250, blank=True ,null=True)
        OrganizationID = models.BigIntegerField(default=0)
        CreatedBy = models.BigIntegerField(default=0)
        CreatedDateTime = models.DateTimeField(default=timezone.now)
        ModifyBy = models.BigIntegerField(default=0)
        ModifyDateTime = models.DateTimeField(default=timezone.now)
        IsDelete = models.BooleanField(default = False)
        def __str__(self):
              return self.Name1 
 

class Project(models.Model):
        Project_Name1=models.CharField(max_length=250, blank=True ,null=True)
        OrganizationID = models.BigIntegerField(default=0)
        CreatedBy = models.BigIntegerField(default=0)
        CreatedDateTime = models.DateTimeField(default=timezone.now)
        ModifyBy = models.BigIntegerField(default=0)
        ModifyDateTime = models.DateTimeField(default=timezone.now)
        IsDelete = models.BooleanField(default = False)
        def __str__(self):
              return self.Project_Name1 
      

class Contract_deta(models.Model):
        Project_Approvel_Request=models.ForeignKey(Project_Approvel_Request,on_delete=models.CASCADE)
        Contract_summary=models.ForeignKey(Contract_summary,on_delete=models.CASCADE)
        
        Deta=models.TextField()
        
        OrganizationID = models.BigIntegerField(default=0)
        CreatedBy = models.BigIntegerField(default=0)
        CreatedDateTime = models.DateTimeField(default=timezone.now)
        ModifyBy = models.BigIntegerField(default=0)
        ModifyDateTime = models.DateTimeField(default=timezone.now)
        IsDelete = models.BooleanField(default = False)
   
        def __str__(self):
           return self.Deta
        

class owner_deta(models.Model):
        Project_Approvel_Request=models.ForeignKey(Project_Approvel_Request,on_delete=models.CASCADE)
        owners=models.ForeignKey(owners,on_delete=models.CASCADE)
        
        Deta2=models.TextField()
        
        OrganizationID = models.BigIntegerField(default=0)
        CreatedBy = models.BigIntegerField(default=0)
        CreatedDateTime = models.DateTimeField(default=timezone.now)
        ModifyBy = models.BigIntegerField(default=0)
        ModifyDateTime = models.DateTimeField(default=timezone.now)
        IsDelete = models.BooleanField(default = False)
   
        def __str__(self):
           return self.Deta2
        

class project_deta(models.Model):
        Project_Approvel_Request=models.ForeignKey(Project_Approvel_Request,on_delete=models.CASCADE)
        Project=models.ForeignKey(Project,on_delete=models.CASCADE)
        
        Deta3=models.TextField()
        
        OrganizationID = models.BigIntegerField(default=0)
        CreatedBy = models.BigIntegerField(default=0)
        CreatedDateTime = models.DateTimeField(default=timezone.now)
        ModifyBy = models.BigIntegerField(default=0)
        ModifyDateTime = models.DateTimeField(default=timezone.now)
        IsDelete = models.BooleanField(default = False)
   
        def __str__(self):
           return self.Deta3






