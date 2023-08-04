from django.db import models

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    order_code = models.CharField(unique=True, max_length=10)
    number_of_different_product = models.IntegerField()
    received_timestamp = models.TextField()
    despatch_timestamp = models.TextField()
    order_time = models.IntegerField()
    def __str__(self):
        return self.order_code

class Carrier(models.Model):
    id = models.IntegerField(primary_key=True)
    order_code = models.CharField(max_length=10)
    carrier_code = models.CharField(unique=True, max_length=20)
    product_code = models.CharField(max_length=8)
    stored_timestamp = models.TextField()
    despatch_timestamp = models.TextField()
    shelf_age = models.IntegerField()
    def __str__(self):
        return self.carrier_code

class Statistic(models.Model):
    id = models.IntegerField(primary_key=True)
    product_code = models.CharField(unique=True, max_length=20)
    total_carrier = models.PositiveBigIntegerField()
    total_shelf_age = models.PositiveBigIntegerField()
    total_cost = models.PositiveBigIntegerField()
    total_price = models.PositiveBigIntegerField()
    total_wage = models.PositiveBigIntegerField()
    total_order = models.PositiveBigIntegerField()
    total_different_day_timestamp = models.IntegerField()
    maximum_demand = models.IntegerField()
    average_demand = models.FloatField()
    minimum_demand = models.IntegerField()
    maximum_flow = models.IntegerField()
    average_flow = models.PositiveBigIntegerField()
    minimum_flow = models.IntegerField()
    frequency = models.FloatField()
    def __str__(self):
        return self.product_code

class Layout(models.Model):
    id = models.IntegerField(primary_key=True)
    identification = models.CharField(unique=True, max_length=6)
    floor = models.CharField(max_length=1)
    section = models.CharField(max_length=1)
    location = models.CharField(max_length=1)
    shelf = models.CharField(max_length=1)
    column = models.CharField(max_length=1)
    row = models.CharField(max_length=1)
    emc = models.BooleanField(default=0)
    def __str__(self):
        return self.identification
  
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    identification = models.CharField(unique=True, max_length=8)
    quantity = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    profit = models.PositiveIntegerField(default=0)
    wage = models.PositiveIntegerField(default=0)
    description = models.TextField(default="N/A")
    def __str__(self):
        return self.identification

class Slot(models.Model):
    id = models.IntegerField(primary_key=True)
    identification = models.CharField(unique=True, max_length=6)
    prefer = models.CharField(max_length=8, default=0)
    empty = models.BooleanField(default=True)
    reserved = models.BooleanField(default=False)
    age = models.BigIntegerField(default=0)
    product = models.CharField(max_length=8)
    carrier = models.CharField(max_length=20)
    order = models.CharField(max_length=20)
    def __str__(self):
        return self.identification