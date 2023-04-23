from django.shortcuts import render, redirect
from expensetracker.models import *
from moneymanager.models import *


def homepage(request):
    allregularmonthlyexpense = regularmonthlyexpense.objects.all()
    allunexpectedmonthlyexpense = unexpectedmonthlyexpense.objects.exclude(
        expenseStatus=False)
    allregularmonthlyincome = regularmonthlyincome.objects.all()
    allmoneyitems = moneymanager.objects.all()

    totalexpense = 0
    totalincome = 0
    totalcashinvested = 0

    for eachExpense in allregularmonthlyexpense:
        totalexpense = eachExpense.expenseAmount + totalexpense

    for eachExpense in allunexpectedmonthlyexpense:
        totalexpense = eachExpense.expenseAmount + totalexpense

    for eachExpense in allregularmonthlyincome:
        totalincome = eachExpense.incomeAmount + totalincome

    for eachCashItem in allmoneyitems:
        totalcashinvested = totalcashinvested + eachCashItem.cashAmount

    moneyleft = totalincome - totalexpense

    return render(request, "index.html", {"totalexpense": totalexpense, "totalincome": totalincome, "moneyleft": moneyleft, "totalcashinvested": totalcashinvested})
