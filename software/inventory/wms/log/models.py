from django.db import models
from datetime import datetime

class  LogOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    identification = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=datetime.now())
    timedespatch = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return self.identification

class  LogCarrier(models.Model):
    id = models.IntegerField(primary_key=True)
    identification = models.CharField(max_length=20)
    receive = models.BooleanField(default=1)
    despatch = models.BooleanField(default=0)
    timestamp = models.DateTimeField(default=datetime.now())
    timedespatch = models.DateTimeField(default=datetime.now())
    coordinate = models.CharField(max_length=6)
    product = models.CharField(max_length=8)
    order = models.CharField(max_length=20)
    def __str__(self):
        return self.identification

class RecordProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    identification = models.CharField(max_length=8)
    p_quantity = models.PositiveIntegerField(default=0)
    p_cost = models.PositiveIntegerField(default=0)
    p_wage = models.PositiveIntegerField(default=0)
    p_emc = models.PositiveBigIntegerField(default=0)
    c_total = models.PositiveIntegerField(default=0)
    c_reserved = models.PositiveIntegerField(default=0)
    c_available = models.PositiveIntegerField(default=0)
    t_order = models.PositiveIntegerField(default=0)
    t_day = models.PositiveIntegerField(default=0)
    t_despatch = models.PositiveBigIntegerField(default=0)
    r_frequency = models.FloatField(default=0)
    r_flow = models.FloatField(default=0)
    r_demand = models.FloatField(default=0)
    s_value = models.PositiveBigIntegerField(default=0)
    s_percentage = models.FloatField(default=0)
    s_assign = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.identification

class StatisticProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    identification = models.CharField(max_length=8)
    year = models.CharField(max_length=4)
    a_order = models.PositiveIntegerField(default=0)
    a_day = models.PositiveIntegerField(default=0)
    a_despatch = models.PositiveBigIntegerField(default=0)
    a_value = models.PositiveBigIntegerField(default=0)
    def __str__(self):
        return self.identification
