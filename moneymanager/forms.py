from django import forms
from .models import moneymanager


class MoneyForm(forms.ModelForm):
    class Meta:
        model = moneymanager
        fields = [
            "cashName",
            "cashType",
            "cashAmount",
            "cashRate",
            "cashStartDate",
            "cashMaturityDate",
        ]
