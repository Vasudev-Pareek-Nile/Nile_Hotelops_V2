from django.db import models
from datetime import date


   
class  FixedSignageMaster(models.Model):
    title = models.CharField(max_length = 200, null=True)
    category = models.CharField(max_length= 200, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
        
class  FixedSignageEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0, null=True)
    EntryYear =models.BigIntegerField(default=0, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    TotalAmount  = models.DecimalField(decimal_places=2,max_digits=12, null=True )
    IsDelete = models.BooleanField(default=False)
     
class  FixedSignageEntryDetails(models.Model):
    FixedSignageMaster =models.ForeignKey(FixedSignageMaster, on_delete=models.CASCADE)
    FixedSignageEntryMaster =models.ForeignKey(FixedSignageEntryMaster, on_delete=models.CASCADE)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
      


   
class  IndicativeProImpMaster(models.Model):
    title = models.CharField(max_length = 200, null=True)
    category = models.CharField(max_length= 200, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False, null=True)
        
class   IndicativeProImpEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0, null=True)
    EntryYear =models.BigIntegerField(default=0, null=True)
    TotalIndProjTimeFrame = models.IntegerField(default=0, null=True)
    Months = models.BigIntegerField(default=0 , null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    TotalAmount  = models.DecimalField(decimal_places=2,max_digits=12, null=True )
    IsDelete = models.BooleanField(default=False)
     
class   IndicativeProImpEntryDetails(models.Model):
    IndicativeProImpMaster =models.ForeignKey(IndicativeProImpMaster, on_delete=models.CASCADE)
    IndicativeProImpEntryMaster =models.ForeignKey(IndicativeProImpEntryMaster, on_delete=models.CASCADE)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
 
 
    
class  DivisionMaster(models.Model):
    title = models.CharField(max_length = 200, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
class  SectionMaster(models.Model):
    title = models.CharField(max_length = 200, null=True)
    DivisionMaster = models.ForeignKey(DivisionMaster , on_delete=models.CASCADE)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)   
    
    def __str__(self) -> str:
        return self.title 
     
class  SnagListMaster(models.Model):
    title = models.CharField(max_length = 1000, null=True)
    SectionMaster = models.ForeignKey(SectionMaster , on_delete=models.CASCADE)
    category = models.CharField(max_length= 200, null=True)
    worktype = models.CharField(max_length= 200, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
        
class   SnagListEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0, null=True)
    EntryYear =models.BigIntegerField(default=0, null=True)
    SectionMaster = models.ForeignKey(SectionMaster , on_delete=models.CASCADE)
    Area = models.CharField(max_length= 200, null=True)
    Date =models.DateField(default = date.today, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
     
     
class   SnagListEntryDetails(models.Model):
    SnagListMaster =models.ForeignKey(SnagListMaster, on_delete=models.CASCADE)
    SnagListEntryMaster =models.ForeignKey(SnagListEntryMaster, on_delete=models.CASCADE)      
    Yes = models.BooleanField()
    Remarks = models.TextField(null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
      


    
class  ProjectImpProcessMaster(models.Model):
    title = models.CharField(max_length = 200, null=True)
    category = models.CharField(max_length= 200, null=True)
    ActionBy = models.CharField(max_length=200, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
        
class   ProjectImpProcessEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0, null=True)
    EntryYear =models.BigIntegerField(default=0, null=True)
    Project = models.CharField(max_length=200, null=True)
    StartDate =models.DateField(default = date.today, null=True)
    ForecastCompletionDate = models.DateField(default=date.today, null=True)
    Attention = models.CharField(max_length=200, null=True)
    Issue = models.CharField(max_length=200, null=True)
    By = models.CharField(max_length=200, null=True)
    Date = models.DateField(default=date.today, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
         
class   ProjectImpProcessEntryDetails(models.Model):
    ProjectImpProcessMaster =models.ForeignKey(ProjectImpProcessMaster, on_delete=models.CASCADE)
    ProjectImpProcessEntryMaster =models.ForeignKey(ProjectImpProcessEntryMaster, on_delete=models.CASCADE) 
    ResponseTime = models.CharField(max_length=200, null=True)
    Remarks = models.CharField(max_length= 200, null=True)
    CompletionBy = models.CharField(max_length= 200, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
     
     
            
class  HotelHandOverMaster(models.Model):
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
          
class  HotelHandOverEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0, null=True)
    EntryYear =models.BigIntegerField(default=0, null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    TotalAmount  = models.DecimalField(decimal_places=2,max_digits=12, null=True )
    IsDelete = models.BooleanField(default=False)
    
    
class   HandOverEntryDetails(models.Model):
    HotelHandOverMaster =models.ForeignKey(HotelHandOverMaster, on_delete=models.CASCADE)
    HotelHandOverEntryMaster =models.ForeignKey(HotelHandOverEntryMaster, on_delete=models.CASCADE)   
    # A = models.BooleanField()
    # B = models.BooleanField()
    # C =  models.BooleanField()
    # D =  models.BooleanField()
    # E =  models.BooleanField()
    # F = models.BooleanField()
    # G =  models.BooleanField()
    # H =  models.BooleanField()
    # I =  models.BooleanField()
    # J =  models.BooleanField()
    # K =  models.BooleanField()
    # L =  models.BooleanField()
    # M =  models.BooleanField()
    # N =  models.BooleanField()
    # O =  models.BooleanField()
    # P =  models.BooleanField()
    # Q =  models.BooleanField()
    # R =  models.BooleanField()
    # S =  models.BooleanField()
    Remarks = models.TextField(null=True)
    OrganizationID = models.BigIntegerField(default=0, null=True)
    CreatedBy = models.BigIntegerField(default=0, null=True)
    CreatedDateTime = models.DateField(default = date.today, null=True)
    ModifyBy = models.BigIntegerField(default=0, null=True)
    ModifyDateTime = models.DateField(default = date.today, null=True)
    IsDelete = models.BooleanField(default=False)
