from django import forms
from .models import *


class RegularMonthlyForm(forms.ModelForm):
    class Meta:
        model = regularmonthlyexpense
        fields = [
            "expenseName",
            "expenseAmount",
            "expenseDate",
        ]


class UnexpectedMonthlyForm(forms.ModelForm):
    class Meta:
        model = unexpectedmonthlyexpense
        fields = [
            "expenseName",
            "expenseAmount",
            "expenseDate",
            "expenseOwesTo",
        ]


class RegularIncomeForm(forms.ModelForm):
    class Meta:
        model = regularmonthlyincome
        fields = [
            "incomeName",
            "incomeAmount",
            "incomeDate",
        ]
