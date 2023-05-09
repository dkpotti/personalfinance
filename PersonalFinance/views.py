from django.shortcuts import render, redirect
from expensetracker.models import *
from moneymanager.models import *
from investmentmanager.models import *
from django.db.models import Sum, Count


def homepage(request):
    allregularmonthlyexpense = regularmonthlyexpense.objects.all()
    allunexpectedmonthlyexpense = unexpectedmonthlyexpense.objects.exclude(
        expenseStatus=False)
    allregularmonthlyincome = regularmonthlyincome.objects.all()
    allmoneyitems = moneymanager.objects.all()

    totalexpense = 0
    totalincome = 0
    totalcashinvested = 0
    expensePercentage = 0
    savingsPercentage = 0
    leftOverPercentage = 0
    investmentPercentage = 0

    totalincome = regularmonthlyincome.objects.aggregate(
        Sum('incomeAmount'))['incomeAmount__sum']
    totalexpense = regularmonthlyexpense.objects.aggregate(
        Sum('expenseAmount'))['expenseAmount__sum']
    totalMonthlySavings = regularmonthlysavings.objects.all().aggregate(
        Sum('savingsAmount'))['savingsAmount__sum']
    totalcashinvested = moneymanager.objects.aggregate(
        Sum('cashAmount'))['cashAmount__sum']
    totalInvestments = monthlyinvestment.objects.aggregate(
        Sum('investmentConverted'))['investmentConverted__sum']

    moneyleft = totalincome - \
        (totalexpense + totalInvestments + totalMonthlySavings)

    expensePercentage = (totalexpense / totalincome) * 100
    savingsPercentage = (totalMonthlySavings / totalincome) * 100
    leftOverPercentage = (moneyleft / totalincome) * 100
    investmentPercentage = (totalInvestments / totalincome) * 100

    return render(request, "index.html", {"totalexpense": totalexpense, "totalincome": totalincome, "moneyleft": moneyleft, "totalcashinvested": totalcashinvested,
                                          "totalInvestments": totalInvestments, "totalMonthlySavings": totalMonthlySavings,
                                          "expensePercentage": expensePercentage, "savingsPercentage": savingsPercentage, "leftOverPercentage": leftOverPercentage, "investmentPercentage": investmentPercentage})
