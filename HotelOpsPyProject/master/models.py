from django.db import models
# For Creating Class Product Master
class Product_Master(models.Model):
    Product = models.CharField(max_length=100)
    Domain_URL = models.CharField(max_length=100)
    ProductLabel = models.CharField(max_length=100)
    Is_Visible =  models.BooleanField(default=True)
    Is_Enable = models.BooleanField(default=True)
    Organization_Id = models.BigIntegerField(default=0)
    Sort_Order = models.CharField(max_length=100)
    Parent_Id =  models.BigIntegerField(default=0)
    Is_Carporate =  models.BooleanField(default=True)
    
    def __str__(self):
        return self.ProductLabel
    
# For Creating Class Product Group Master
class Product_Group_Master(models.Model):
    Group = models.CharField(max_length=100)
    Is_Visible = models.BooleanField(default=True)
    Is_Enable =  models.BooleanField(default=True)
    Sort_Order = models.CharField(max_length=100)
    Organization_Id = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.Group
    
# For Creating Class Product Group Mapping
class Product_Group_Mapping(models.Model):
    Product_Master = models.ForeignKey(Product_Master, on_delete=models.CASCADE)
    Product_Group_Master = models.ForeignKey(Product_Group_Master, on_delete=models.CASCADE)
    def __str__(self):
        return (str(self.Product_Master)+" - "+str(self.Product_Group_Master))

    
    

    

