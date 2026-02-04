from django.db import models
from datetime import date


class Entry_Master_Year(models.Model):
    EntryYear = models.IntegerField()    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return f"EntryMaster ID: {self.id}, EntryYear: {self.EntryYear}"



class  Finance_Category(models.Model):
    Finance_category = models.CharField(max_length=255,null=False,blank=False)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Finance_category
    class Meta:
        ordering = ['id']
    



class Finance_Category_Entry_Details(models.Model):
    EntryMaster = models.ForeignKey(Entry_Master_Year,on_delete=models.CASCADE,null=False,blank=False)
    Finance_Category_Name = models.ForeignKey(Finance_Category,  on_delete=models.CASCADE,null=False,blank=False)

    Month_1=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_2=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_3=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_4=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_5=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_6=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_7=models.DecimalField (max_digits=12, decimal_places=2,null=True,blank=False)
    Month_8=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_9=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_10=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_11=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_12=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
        
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
         return f"EntryMaster ID: {self.id}, EntryYear: {self.Finance_Category_Name}"
     



class Market_Segment_Category(models.Model):
    market_segment_category = models.CharField(max_length=255,null=False,blank=False)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.market_segment_category
    class Meta:
        ordering = ['id']
    



class Market_Segment_Entry_Details(models.Model):
    EntryMaster = models.ForeignKey(Entry_Master_Year,on_delete=models.CASCADE,null=False,blank=False)
    Market_Segment_Category_Name = models.ForeignKey(Market_Segment_Category,  on_delete=models.CASCADE,null=False,blank=False)

    Month_1=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_2=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_3=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_4=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_5=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_6=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_7=models.DecimalField (max_digits=12, decimal_places=2,null=True,blank=False)
    Month_8=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_9=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_10=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_11=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_12=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
        
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
         return f"EntryMaster ID: {self.id}, EntryYear: {self.Market_Segment_Category_Name}"
    


class Business_Source_Category(models.Model):
    business_source_category = models.CharField(max_length=255,null=False,blank=False)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.business_source_category
    class Meta:
        ordering = ['id']
    



class Business_Source_Entry_Details(models.Model):
    EntryMaster = models.ForeignKey(Entry_Master_Year,on_delete=models.CASCADE,null=False,blank=False)
    Business_Source_Category_Name = models.ForeignKey(Business_Source_Category,  on_delete=models.CASCADE,null=False,blank=False)

    Month_1=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_2=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_3=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_4=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_5=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_6=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_7=models.DecimalField (max_digits=12, decimal_places=2,null=True,blank=False)
    Month_8=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_9=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_10=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_11=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_12=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
        
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
         return f"EntryMaster ID: {self.id}, EntryYear: {self.Business_Source_Category_Name}"





class ExpensesIncludingPayroll(models.Model):
    Title = models.CharField(max_length=255,null=False,blank=False)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Title
    class Meta:
        ordering = ['id']





class ExpensesIncludingPayrollEntryDetails(models.Model):
    EntryMaster = models.ForeignKey(Entry_Master_Year,on_delete=models.CASCADE,null=False,blank=False)
    ExpensesIncludingPayroll = models.ForeignKey(ExpensesIncludingPayroll,  on_delete=models.CASCADE,null=False,blank=False)

    Month_1=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_2=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_3=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_4=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_5=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_6=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_7=models.DecimalField (max_digits=12, decimal_places=2,null=True,blank=False)
    Month_8=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_9=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_10=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_11=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_12=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
        
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
         return f"EntryMaster ID: {self.id}, EntryYear: {self.ExpensesIncludingPayroll}"








class CostPerCover(models.Model):
    Title = models.CharField(max_length=255,null=False,blank=False)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Title
    class Meta:
        ordering = ['id']





class CostPerCoverEntryDetails(models.Model):
    EntryMaster = models.ForeignKey(Entry_Master_Year,on_delete=models.CASCADE,null=False,blank=False)
    CostPerCover = models.ForeignKey(CostPerCover,  on_delete=models.CASCADE,null=False,blank=False)

    Month_1=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_2=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_3=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_4=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_5=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_6=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_7=models.DecimalField (max_digits=12, decimal_places=2,null=True,blank=False)
    Month_8=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_9=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_10=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_11=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_12=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
        
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
         return f"EntryMaster ID: {self.id}, EntryYear: {self.CostPerCover}"




class CostPerOccupiedRoomNight(models.Model):
    Title = models.CharField(max_length=255,null=False,blank=False)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Title
    class Meta:
        ordering = ['id']





class CostPerOccupiedRoomNightEntryDetails(models.Model):
    EntryMaster = models.ForeignKey(Entry_Master_Year,on_delete=models.CASCADE,null=False,blank=False)
    CostPerOccupiedRoomNight = models.ForeignKey(CostPerOccupiedRoomNight,  on_delete=models.CASCADE,null=False,blank=False)

    Month_1=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_2=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_3=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_4=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_5=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_6=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_7=models.DecimalField (max_digits=12, decimal_places=2,null=True,blank=False)
    Month_8=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_9=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_10=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_11=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_12=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
        
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
         return f"EntryMaster ID: {self.id}, EntryYear: {self.CostPerOccupiedRoomNight}"



class Engineering_Category(models.Model):
    Engineering_category = models.CharField(max_length=255,null=False,blank=False)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Engineering_category
    class Meta:
        ordering = ['id']
    


class Engineering_Category_Entry_Details(models.Model):
    EntryMaster = models.ForeignKey(Entry_Master_Year,on_delete=models.CASCADE,null=False,blank=False)
    Engineering_Category_Name = models.ForeignKey(Engineering_Category,  on_delete=models.CASCADE,null=False,blank=False)

    Month_1=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_2=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_3=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_4=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_5=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_6=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_7=models.DecimalField (max_digits=12, decimal_places=2,null=True,blank=False)
    Month_8=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_9=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_10=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_11=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
    Month_12=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=False)
        
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
         return f"EntryMaster ID: {self.id}, EntryYear: {self.Engineering_Category_Name}"
     