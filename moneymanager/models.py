from django.db import models
from django.utils import timezone

# Create your models here.


class moneymanager(models.Model):
    cashName = models.CharField(max_length=50)
    cashType = models.CharField(max_length=50)
    cashAmount = models.DecimalField(max_digits=6, decimal_places=2)
    cashRate = models.DecimalField(max_digits=6, decimal_places=2)
    cashStartDate = models.DateField(default=timezone.now)
    cashMaturityDate = models.DateField(default=timezone.now)

    def __str__(self):
        return self.cashName
