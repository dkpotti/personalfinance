from django.db import models
from django.utils import timezone

# Create your models here.


class monthlyinvestment(models.Model):
    investmentName = models.CharField(max_length=50)
    investmentAmount = models.DecimalField(max_digits=6, decimal_places=2)
    investmentDate = models.DateField(default=timezone.now)

    def __str__(self):
        return self.investmentName
