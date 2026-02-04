from django.db import models
from datetime import date
# Create your models here.
class VerbalWarningmoduls(models.Model):
    emp_code = models.CharField(max_length=255, blank=True, null=True)
    emp_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    problems = models.TextField(blank=True, null=True)
    improvements = models.TextField(blank=True, null=True)
    from_date = models.DateField( blank=True, null=True)
    to_date = models.DateField( blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=200, blank=True, null=True)
    verbally_warned = models.DateField(blank=True, null=True)
    appeal_explained = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], blank=True, null=True)
    appeal = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], blank=True, null=True)
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)
    associate_signature_date = models.DateField( blank=True, null=True)
    manager_signature_date = models.DateField( blank=True, null=True)

    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    

    def __str__(self):
        return self.emp_name
    


class WrittenWarningModul(models.Model):
    employee_no = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    
    
    warnings_choices = [
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third'),
    ]
    warnings = models.CharField(max_length=20, choices=warnings_choices)

    problems = models.TextField()
    written_warning = models.TextField()
    improvements = models.TextField()
    period_from = models.DateField()
    period_to = models.DateField()
    warning_date = models.DateField()
    warning_time = models.TimeField()
    witnesses = models.TextField(blank=True, null=True)

    appeal = models.CharField(max_length=50, blank=True, null=True)
    agree_with_warning = models.BooleanField(default=False)
    disagree_with_warning = models.BooleanField(default=False)

    supervisor_signature_date = models.DateField()
    associate_signature_date = models.DateField()
    reviewed_by = models.CharField(max_length=100)
    seen_by = models.CharField(max_length=100)
    DepartmentManager = models.DateField()
    hr_manager_signature_date = models.DateField()

    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.employee_no
    

class FinalWarningModule(models.Model):
    employee_no = models.CharField(max_length=20,null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    department = models.CharField(max_length=100,null=True, blank=True)
    designation = models.CharField(max_length=100,null=True, blank=True)
    warning_type = models.CharField(max_length=50,null=True, blank=True)
    employee_problem = models.TextField(null=True, blank=True)
    written_warning = models.TextField(null=True, blank=True)
    improvement_standard = models.TextField(null=True, blank=True)
    improvement_period_from = models.DateField(null=True, blank=True)
    improvement_period_to = models.DateField(null=True, blank=True)
    warning_date = models.DateField(null=True, blank=True)
    warning_time = models.TimeField(null=True, blank=True)
    witness = models.CharField(max_length=255,null=True, blank=True)
    appeal = models.CharField(max_length=10,null=True, blank=True)
    agree_warning = models.BooleanField(default=False,null=True, blank=True)
    disagree_warning = models.BooleanField(default=False,null=True, blank=True)
    supervisor_signature_date = models.DateField(null=True, blank=True)
    associate_signature_date = models.DateField(null=True, blank=True)
    reviewed_by = models.CharField(max_length=100, blank=True)
    department_signature_date = models.DateField(null=True, blank=True)
    hr_manager_signature = models.CharField(max_length=100, blank=True)
    
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return f"Final Warning for {self.name}"


class WarningMasterDetail(models.Model):
    Empcode =  models.CharField(max_length=20)
    Lastwarningtype = models.CharField(max_length=20)
    OrganizationID = models.BigIntegerField()
    CreatedByUsername = models.CharField(max_length=255, blank=True, null=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)    

    