from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'category'  # Use the existing table name


class Farm(models.Model):
    farm_name = models.CharField(max_length=255)
    address = models.TextField()
    inventory = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'farm'  # Use the existing table name


class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    unit = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'item'  # Use the existing table name