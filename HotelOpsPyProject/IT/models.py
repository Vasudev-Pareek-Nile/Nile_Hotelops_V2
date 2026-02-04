from django.db import models
from datetime import datetime


class ItInformation(models.Model):
    EmployeeName = models.CharField(max_length=255, null=True)
    EmployeeCode = models.CharField(max_length=255, null=True)
    DesignationGrade = models.CharField(max_length=255, null=True)
    Department = models.CharField(max_length=255, null=True)
    HotelOpsAccount = models.CharField(max_length=255, null=True, blank=True)
    IsClosed = models.BooleanField(default=False)

    
    HrStatus = models.CharField(max_length=255, null=True, default='0')
    HrComment = models.CharField(max_length=255, null=True)

    ItStatus = models.CharField(max_length=255, null=True, default='0')
    ItComment = models.CharField(max_length=255, null=True)

    HodStatus = models.CharField(max_length=255, null=True, default='0')
    HodComment = models.CharField(max_length=255, null=True)
    
    ReportingtoDesigantion=models.CharField(max_length=255,null=False,blank=False)

    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)



class SimDetail(models.Model):
    ItInformation = models.ForeignKey(ItInformation, on_delete=models.CASCADE)
    DateofRequest = models.DateTimeField(null=True)
    DateofIssue = models.DateTimeField(null=True)
    MobileNo = models.CharField(max_length=255, null=True)
    RequestedBy =  models.CharField(max_length=255, null=True)
    IsIssued = models.BooleanField(default=False)
    IsReturned = models.BooleanField(default=False)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)

class MobileDetail(models.Model):
    ItInformation = models.ForeignKey(ItInformation, on_delete=models.CASCADE)
    DateofRequest = models.DateTimeField(null=True)
    DateofIssue = models.DateTimeField(null=True)
    CompanyName = models.CharField(max_length=255, null=True) 
    ModelNumber = models.CharField(max_length=255, null=True)
    IMEINumber = models.CharField(max_length=255, null=True)
    Colour = models.CharField(max_length=255, null=True)
    RequestedBy =  models.CharField(max_length=255, null=True)
    IsIssued = models.BooleanField(default=False)
    IsReturned = models.BooleanField(default=False)

    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)


class EmailDetail(models.Model):
    ItInformation = models.ForeignKey(ItInformation, on_delete=models.CASCADE)
    DateofRequest = models.DateTimeField(null=True)
    DateofIssue = models.DateTimeField(null=True)
    Email = models.CharField(max_length=255, null=True) 
    Type = models.CharField(max_length=255, null=True) 
    DomainType = models.CharField(max_length=255, null=True) 
    RequestedBy =  models.CharField(max_length=255, null=True)
    IsIssued = models.BooleanField(default=False)
    IsReturned = models.BooleanField(default=False)

    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)


class SystemDetail(models.Model):
    ItInformation = models.ForeignKey(ItInformation, on_delete=models.CASCADE)
    DateofRequest = models.DateTimeField(null=True)
    DateofIssue = models.DateTimeField(null=True)
    SystemType = models.CharField(max_length=255, null=True) 
    CompanyName = models.CharField(max_length=255, null=True) 
    ModelNumber = models.CharField(max_length=255, null=True)
    SerialNumber = models.CharField(max_length=255, null=True)
    Configuration = models.TextField(null=True,blank=True)
    RequestedBy =  models.CharField(max_length=255, null=True)
    IsIssued = models.BooleanField(default=False)
    IsReturned = models.BooleanField(default=False)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)

   




