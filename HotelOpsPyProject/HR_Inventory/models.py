from django.db import models
from django.utils import timezone

# -- Main Employee Info Details here
class HR_Inventory_Information(models.Model):
    EmpID = models.BigIntegerField(default=0, null=True, blank=True)
    EmployeeName = models.CharField(max_length=255, null=True)
    EmployeeCode = models.CharField(max_length=255, null=True)
    DesignationGrade = models.CharField(max_length=255, null=True)
    Department = models.CharField(max_length=255, null=True)
    ReportingtoDesigantion=models.CharField(max_length=255,null=False,blank=False)

    HrStatus = models.CharField(max_length=255, null=True, default='0')
    HrComment = models.CharField(max_length=255, null=True)

    HousekeppingStatus = models.CharField(max_length=255, null=True, default='0')
    HousekeppingComment = models.CharField(max_length=255, null=True)

    HodStatus = models.CharField(max_length=255, null=True, default='0')
    HodComment = models.CharField(max_length=255, null=True)
   
   
    Return = models.BooleanField(default=False)
    ReturnAmount = models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=True)

    HR = models.BooleanField(default=False)
    HRCreatedBy = models.BigIntegerField(default=0)
    
    
    IssuedDate = models.DateField(default=timezone.now)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



# -- All Iteams Here
class HR_Inventory_Item_Master(models.Model):
    ItemName = models.CharField(max_length=255, null=True)
    Price = models.DecimalField( max_digits=12, decimal_places=2)
    Year = models.IntegerField(null=False,blank=False)  
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)





# -- Rest of uniform data here
class HR_Inventory_Details(models.Model):
    HR_Inventory_Information = models.ForeignKey(HR_Inventory_Information, on_delete=models.CASCADE)
    HR_Inventory_Item_Master = models.ForeignKey(HR_Inventory_Item_Master, on_delete=models.CASCADE)
    
    Item_Issued = models.CharField(max_length=255, null=True)
    Item_Returned = models.CharField(max_length=255, null=True)

    TotalCharged = models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




