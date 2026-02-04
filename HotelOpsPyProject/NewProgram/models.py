from django.db import models
from datetime import date 
from django.utils import timezone
from django.utils import timezone

# Create your models here.
class area(models.Model):
    area_name = models.CharField(max_length=250)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.area_name
    

class Location(models.Model):
    arean = models.CharField(max_length=250)
    location_name=models.CharField(max_length=250, blank=True ,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.location_name
    

class project_review(models.Model):
    project=models.CharField(max_length=250, blank=True ,null=True)
    title=models.CharField(max_length=250, blank=True ,null=True)
    height_bulding = models.CharField(max_length=250, blank=True ,null=True)
    structure_type=models.CharField(max_length=250, blank=True ,null=True)
    total_area=models.CharField(max_length=250, blank=True ,null=True)
    structure_levels=models.CharField(max_length=250, blank=True ,null=True)
    built_area=models.CharField(max_length=250, blank=True ,null=True)
    no_of_room=models.CharField(max_length=250, blank=True ,null=True)
    guest_size=models.CharField(max_length=250, blank=True ,null=True)
    room_mix=models.CharField(max_length=250, blank=True ,null=True)
    lenth=models.CharField(max_length=250, blank=True ,null=True)
    barth=models.CharField(max_length=250, blank=True ,null=True)
    net=models.CharField(max_length=250, blank=True ,null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.height_bulding



class Front_admin(models.Model):
      Title=models.CharField(max_length=250, blank=True ,null=True)
      name=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.Title
      



class front_perent(models.Model):
      
      name=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.name












class front_subchild(models.Model):
      
      Sub_name=models.CharField(max_length=250, blank=True ,null=True)

      name1=models.CharField(max_length=250, blank=True ,null=True)
      

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.Sub_name
      

class front_child(models.Model):
      
      child_name=models.CharField(max_length=250, blank=True ,null=True)


      

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.child_name   


from datetime import datetime
class Front_of_House(models.Model):
      date=models.DateField(default=timezone.now)
      location=models.CharField(max_length=250, blank=True ,null=True)
      project_number=models.CharField(max_length=250, blank=True ,null=True)
      hotel_key=models.CharField(max_length=250, blank=True ,null=True)
      guest_room_floors=models.CharField(max_length=250, blank=True ,null=True)
      hotel_bays=models.CharField(max_length=250, blank=True ,null=True)
      reqvered_parking_spaces=models.CharField(max_length=250, blank=True ,null=True)

      

      Region_name=models.CharField(max_length=250, blank=True ,null=True)

      Location_Index=models.CharField(max_length=250, blank=True ,null=True)
      Parking_Required=models.CharField(max_length=250, blank=True ,null=True)
      Swimming_Pool=models.CharField(max_length=250, blank=True ,null=True)
      Parking_Levels=models.CharField(max_length=250, blank=True ,null=True)
      Structural_System=models.CharField(max_length=250, blank=True ,null=True)
      Corridor_Requirements=models.CharField(max_length=250, blank=True ,null=True)
      Security_Requirements=models.CharField(max_length=250, blank=True ,null=True)
      Meeting_Space=models.CharField(max_length=250, blank=True ,null=True)
      Feed_Employees=models.CharField(max_length=250, blank=True ,null=True)
      Stairwells=models.CharField(max_length=250, blank=True ,null=True)
      Laundry_Services=models.CharField(max_length=250, blank=True ,null=True)
      Guest_Transportation=models.CharField(max_length=250, blank=True ,null=True)
      Uniform_Distribution=models.CharField(max_length=250, blank=True ,null=True)

      totalroom=models.CharField(max_length=250, blank=True ,null=True)
      totalkey=models.CharField(max_length=250, blank=True ,null=True)
      guestroom=models.CharField(max_length=250, blank=True ,null=True)
      lobbytotal=models.CharField(max_length=250, blank=True ,null=True)
      mettingtotal=models.CharField(max_length=250, blank=True ,null=True)
      additionaltotal=models.CharField(max_length=250, blank=True ,null=True)
      administrativetotal=models.CharField(max_length=250, blank=True ,null=True)



      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateTimeField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateTimeField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.project_number






class front_public_area(models.Model):
      
      public1=models.CharField(max_length=250, blank=True ,null=True)

      public2=models.CharField(max_length=250, blank=True ,null=True)
      

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.public1 



class front_administrative(models.Model):
      
      administrative=models.CharField(max_length=250, blank=True ,null=True)

      
      

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.administrative



# squermeeter 

class Frontss_details(models.Model):
      Front_admin=models.ForeignKey(Front_admin,on_delete=models.CASCADE)
      Front_of_House=models.ForeignKey(Front_of_House,on_delete=models.CASCADE)
      
      squermitter=models.CharField(max_length=250, blank=True ,null=True)
      
      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
   
      def __str__(self):
         return self.squermitter



class guest_room(models.Model):
      Front_of_House=models.ForeignKey(Front_of_House,on_delete=models.CASCADE,blank=True ,null=True)
      front_perent=models.ForeignKey(front_perent,on_delete=models.CASCADE,blank=True ,null=True)

      roomkey=models.CharField(max_length=250, blank=True ,null=True)
      totalSquer=models.CharField(max_length=250, blank=True ,null=True)
      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
   
      def __str__(self):
         return self.roomkey


class lobby(models.Model):
      Front_of_House=models.ForeignKey(Front_of_House,on_delete=models.CASCADE,blank=True ,null=True)
      front_subchild=models.ForeignKey(front_subchild,on_delete=models.CASCADE,blank=True ,null=True)
      lobbysquermeter=models.CharField(max_length=250, blank=True ,null=True)

      
      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.lobbysquermeter

        
class metting_details(models.Model):
      Front_of_House=models.ForeignKey(Front_of_House,on_delete=models.CASCADE,blank=True ,null=True)
      front_child=models.ForeignKey(front_child,on_delete=models.CASCADE,blank=True ,null=True)
      mettingsquer=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.mettingsquer
    

class publicarea_details(models.Model):
      Front_of_House=models.ForeignKey(Front_of_House,on_delete=models.CASCADE,blank=True ,null=True)
      front_public_area=models.ForeignKey(front_public_area,on_delete=models.CASCADE,blank=True ,null=True)
      public_squermeter=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.public_squermeter
      

class administrative_details(models.Model):
      Front_of_House=models.ForeignKey(Front_of_House,on_delete=models.CASCADE,blank=True ,null=True)
      front_administrative=models.ForeignKey(front_administrative,on_delete=models.CASCADE,blank=True ,null=True)
      administartive_squermeter=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.administartive_squermeter
             

class Notes1(models.Model):
      Notes_name1=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.Notes_name1
      
class Notes2(models.Model):
      Notes_name2=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.Notes_name2   


class Notes3(models.Model):
      Notes_name3=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.Notes_name3           
    
class Notes4(models.Model):
      Notes_name4=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.Notes_name4 



class Notes5(models.Model):
      Notes_name5=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.Notes_name5     


class Notes6(models.Model):
      Notes_name6=models.CharField(max_length=250, blank=True ,null=True)

      OrganizationID = models.BigIntegerField(default=0)
      CreatedBy = models.BigIntegerField(default=0)
      CreatedDateTime = models.DateField(default=timezone.now)
      ModifyBy = models.BigIntegerField(default=0)
      ModifyDateTime = models.DateField(default=timezone.now)
      IsDelete = models.BooleanField(default=False)
      def __str__(self):
         return self.Notes_name6           

