from django.shortcuts import render, redirect
from .models import *
from .forms import *
from moneymanager.models import *
from django.db.models import Sum, Count


# Create your views here.


def viewexpense(request):
    allregularmonthlyexpense = regularmonthlyexpense.objects.all()
    allregularmonthlysavings = regularmonthlysavings.objects.all()
    allunexpectedmonthlyexpense = unexpectedmonthlyexpense.objects.exclude(
        expenseStatus=False)
    allregularmonthlyincome = regularmonthlyincome.objects.all()

    totalRegularExpense = regularmonthlyexpense.objects.aggregate(
        Sum('expenseAmount'))['expenseAmount__sum']
    totalMonthlyIncome = regularmonthlyincome.objects.aggregate(
        Sum('incomeAmount'))['incomeAmount__sum']
    totalSavings = regularmonthlysavings.objects.all().aggregate(
        Sum('savingsAmount'))['savingsAmount__sum']

    totalSavings = (totalSavings/totalMonthlyIncome) * 100
    expensePercentage = (totalRegularExpense/totalMonthlyIncome) * 100
    leftOverPercentage = ((totalMonthlyIncome -
                          (totalSavings+totalRegularExpense)) / totalMonthlyIncome) * 100

    return render(request, "viewexpense.html", {"allregularmonthlyexpense": allregularmonthlyexpense, "allunexpectedmonthlyexpense":
                                                allunexpectedmonthlyexpense, "allregularmonthlyincome": allregularmonthlyincome,
                                                "totalRegularExpense": totalRegularExpense, "totalMonthlyIncome": totalMonthlyIncome,
                                                "expensePercentage": expensePercentage, "totalSavings": totalSavings, "allregularmonthlysavings": allregularmonthlysavings,
                                                "leftOverPercentage": leftOverPercentage})


def addregularexpense(request):
    if request.method == "POST":
        form = RegularMonthlyForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("viewexpense")
    else:
        return render(request, "addregularexpense.html", {})


def addunexpectedexpense(request):
    if request.method == "POST":
        form = UnexpectedMonthlyForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("viewexpense")
    else:
        return render(request, "addunexpectedexpense.html", {})


def addregularincome(request):
    if request.method == "POST":
        form = RegularIncomeForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("viewexpense")
    else:
        return render(request, "addregularincome.html", {})


def removeunexpectedexpense(request, item_id):
    item = unexpectedmonthlyexpense.objects.filter(
        pk=item_id).update(expenseStatus=False)

    return redirect("viewexpense")
