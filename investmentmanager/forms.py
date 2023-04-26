from django import forms
from .models import *


class MonthlyInvestmentForm(forms.ModelForm):
    class Meta:
        model = monthlyinvestment
        investmentAmount = forms.DecimalField(initial=0.0)
        fields = "__all__"
