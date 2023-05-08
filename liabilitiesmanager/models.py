from django.db import models
from django.utils import timezone

# Create your models here.


class liabilities (models.Model):
    liabilityName = models.CharField(max_length=50)
    liabilityAmount = models.DecimalField(max_digits=6, decimal_places=2)
    liabilityDate = models.DateField(default=timezone.now)
    liabilityTo = models.CharField(max_length=50)
    liabilityStatus = models.BooleanField(default=True)

    def __str__(self):
        return self.liabilityName
