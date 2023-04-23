from django.db import models
from django.utils import timezone

# Create your models here.


class regularmonthlyexpense(models.Model):
    expenseName = models.CharField(max_length=50)
    expenseAmount = models.DecimalField(max_digits=6, decimal_places=2)
    expenseDate = models.DateField(default=timezone.now)

    def __str__(self):
        return self.expenseName


class unexpectedmonthlyexpense(models.Model):
    expenseName = models.CharField(max_length=50)
    expenseAmount = models.DecimalField(max_digits=6, decimal_places=2)
    expenseDate = models.DateField(default=timezone.now)
    expenseOwesTo = models.CharField(max_length=50)
    expenseStatus = models.BooleanField(default=True)

    def __str__(self):
        return self.expenseName


class regularmonthlyincome(models.Model):
    incomeName = models.CharField(max_length=50)
    incomeAmount = models.DecimalField(max_digits=6, decimal_places=2)
    incomeDate = models.DateField(default=timezone.now)

    def __str__(self):
        return self.incomeName


class regularmonthlysavings(models.Model):
    savingsName = models.CharField(max_length=50)
    savingsAmount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.savingsName
