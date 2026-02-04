from django.db import models
from datetime import date
class NotificationMessageDump(models.Model):
    ModuleName = models.CharField(max_length=255, null=True, blank=True)
    Email = models.TextField(null=True, blank=True) 
    EmailMessageBody = models.TextField(null=True, blank=True)
    AppTitle  = models.CharField(max_length=255, null=True, blank=True)
    AppBody = models.TextField(null=True, blank=True)
    AppUserID = models.TextField(null=True, blank=True) 
    DashboardTitle  = models.CharField(max_length=255, null=True, blank=True)
    DashboardBody = models.TextField(null=True, blank=True)
    DashboardUserID = models.TextField(null=True, blank=True)  
    DashboardIsView = models.BooleanField(default=False)
    RetrunUrl = models.URLField(max_length=500, null=True, blank=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def set_emails(self, emails):
        self.Email = ','.join(emails)

    def get_emails(self):
        return self.Email.split(',') if self.Email else []

    def set_app_user_ids(self, user_ids):
        self.AppUserID = ','.join(map(str, user_ids))

    def get_app_user_ids(self):
        return list(map(int, self.AppUserID.split(','))) if self.AppUserID else []

    def set_dashboard_user_ids(self, user_ids):
        self.DashboardUserID = ','.join(map(str, user_ids))

    def get_dashboard_user_ids(self):
        return list(map(int, self.DashboardUserID.split(','))) if self.DashboardUserID else []
