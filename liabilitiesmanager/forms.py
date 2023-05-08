from django import forms
from .models import *


class LiabilitiesForm(forms.ModelForm):
    class Meta:
        model = liabilities
        fields = ['liabilityName', 'liabilityAmount',
                  'liabilityDate', 'liabilityTo', 'liabilityStatus']
