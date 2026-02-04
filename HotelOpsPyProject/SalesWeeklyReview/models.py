from django.db import models
from datetime import date


  
class  MarketSegmentMaster(models.Model):
    title = models.CharField(max_length = 200)
    category = models.CharField(max_length=200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class  MarketSegmentEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    EntryWeek = models.BigIntegerField(default=0)
    Total = models.DecimalField(decimal_places=2,max_digits=12 )
    TotalRevenue = models.DecimalField(decimal_places=2 , max_digits= 12 , default=0)
    TotalADR = models.DecimalField(decimal_places=2, max_digits= 12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
  
class  MarketSegmentEntryDetails(models.Model):
    MarketSegmentMaster =models.ForeignKey(MarketSegmentMaster, on_delete=models.CASCADE)
    MarketSegmentEntryMaster =models.ForeignKey(MarketSegmentEntryMaster, on_delete=models.CASCADE)
    RoomNights = models.DecimalField(decimal_places=2,max_digits=12)
    Revenue =  models.DecimalField(decimal_places=2,max_digits=12)
    ADR =  models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    

  
class  SourceMaster(models.Model):
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class  SourceEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    Total = models.DecimalField(decimal_places=2,max_digits=12 )
    TotalRevenue = models.DecimalField(decimal_places=2, max_digits= 12 ,default=0)
    TotalADR =  models.DecimalField(decimal_places=2, max_digits= 12 ,default=0)
    TotalRPD =  models.DecimalField(decimal_places=2, max_digits= 12 ,default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
  
class  SourceEntryDetails(models.Model):
    SourceMaster =models.ForeignKey(SourceMaster, on_delete=models.CASCADE)
    SourceEntryMaster =models.ForeignKey(SourceEntryMaster, on_delete=models.CASCADE)
    RMNights = models.DecimalField(decimal_places=2,max_digits=12)
    Revenue =  models.DecimalField(decimal_places=2,max_digits=12)
    ADR =  models.DecimalField(decimal_places=2,max_digits=12)
    RPD =  models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    

  
class  OTAMaster(models.Model):
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class  OTAEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    Total = models.DecimalField(decimal_places=2,max_digits=12 )
    TotalRevenue = models.DecimalField(decimal_places=2 , max_digits=12 , default=0)
    TotalARR =  models.DecimalField(decimal_places=2 , max_digits=12 , default=0)
    TotalRPD =  models.DecimalField(decimal_places=2 , max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
  
class  OTAEntryDetails(models.Model):
    OTAMaster =models.ForeignKey(OTAMaster, on_delete=models.CASCADE)
    OTAEntryMaster =models.ForeignKey(OTAEntryMaster, on_delete=models.CASCADE)
    RoomNights = models.DecimalField(decimal_places=2,max_digits=12)
    RoomRevenue =  models.DecimalField(decimal_places=2,max_digits=12)
    ARR =  models.DecimalField(decimal_places=2,max_digits=12)
    RPD =  models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    

  
class  TravelAgentMaster(models.Model):
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class  TravelAgentEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
  
class  TravelAgentEntryDetails(models.Model):
    TravelAgentMaster =models.ForeignKey(TravelAgentMaster, on_delete=models.CASCADE)
    TravelAgentEntryMaster =models.ForeignKey(TravelAgentEntryMaster, on_delete=models.CASCADE)
    RoomNights = models.DecimalField(decimal_places=2,max_digits=12)
    RoomRevenue =  models.DecimalField(decimal_places=2,max_digits=12)
    ARR =  models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    
  
class CompanyProductivityMaster(models.Model):
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class  CompanyProductivityEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
  
class  CompanyProductivityEntryDetails(models.Model):
    CompanyProductivityMaster =models.ForeignKey(CompanyProductivityMaster, on_delete=models.CASCADE)
    CompanyProductivityEntryMaster =models.ForeignKey(CompanyProductivityEntryMaster, on_delete=models.CASCADE)
    RoomNights = models.DecimalField(decimal_places=2,max_digits=12)
    RoomRevenue =  models.DecimalField(decimal_places=2,max_digits=12)
    ARR =  models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    

