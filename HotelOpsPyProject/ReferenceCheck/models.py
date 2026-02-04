from django.db import models
from datetime import date

# For creating Model for Reference Registration Form
class Reference_Registration_Form(models.Model):
    Applicant_Name  = models.CharField(max_length=100)
    From = models.DateField(default = date.today)
    To = models.DateField(default = date.today)
    Referee_Company_Name = models.CharField(max_length=100)
    Final_Position = models.CharField(max_length=100)
    Refeere_Name =  models.CharField(max_length=100)
    type = (
        ('Yes','Yes'),
        ('NA','NA'),
    )
    Did_You_Directly_Supervise = models.CharField(max_length=50,choices=type,blank=False, null=False)
    Refeere_Position =  models.CharField(max_length=100)
    Refeere_Phone_No =  models.CharField(max_length=100)
    Overall_Performance = models.TextField()
    Strenght = models.TextField()
    Weaknesses = models.TextField()
    What_is_Best_Way_To_Manage_This_Candidate = models.TextField()
    What_Would_His_Supervisor_Say_About_Him = models.TextField()
    What_Would_His_Peers_Say_About_Him = models.TextField()
    Development_Areas = models.TextField()
    Reason_For_Leaving  = models.TextField()
    Would_You_ReHire_This_Person = models.CharField(max_length=50,choices=type,blank=False, null=False)
    Checked_By = models.CharField(max_length=100)
    Date = models.DateField(default = date.today)
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    
    def __str__(self):
        return self.Applicant_Name
    
# # For Making class On The Job Preference
class Job_Preference_Master(models.Model):
    Preference_Name = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.Preference_Name
    
    
# For Creating Reference Form Details
class Reference_formdetails(models.Model):
    Reference_Registration_Form = models.ForeignKey(Reference_Registration_Form, on_delete=models.CASCADE)
    Job_Preference_Master = models.ForeignKey(Job_Preference_Master, on_delete=models.CASCADE)
    Habits = models.CharField(max_length=100)
   
    
    
    def __str__(self):
        return self.Habits
    
    
    
    
    
    
    
