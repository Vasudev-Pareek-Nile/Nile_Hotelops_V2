from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as per your requirements

    def __str__(self):
        return self.name

class ProductGroup(models.Model):
    name = models.CharField(max_length=100)
    Product = models.ManyToManyField(Product)
    # Add other fields as per your requirements

    def __str__(self):
        return self.name