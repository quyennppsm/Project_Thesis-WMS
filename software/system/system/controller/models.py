from django.db import models


class Product(models.Model):
    identification = models.CharField(max_length=10)
    number = models.PositiveBigIntegerField()
    cost = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    profit = models.PositiveIntegerField()
    wage = models.PositiveBigIntegerField()
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.identification

class Coordinate(models.Model):
    position = models.CharField(max_length=10)
    def __str__(self):
        return self.position

class Statistic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    c_stored = models.PositiveBigIntegerField()
    c_reserved = models.PositiveBigIntegerField()
    c_available = models.PositiveBigIntegerField()
    x_oldest = models.CharField(max_length=10)
    x_youngest = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.product} {self.c_store} {self.c_reserved} {self.c_available} {self.x_oldest} {self.x_youngest}"