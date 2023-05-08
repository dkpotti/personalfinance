from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from moneymanager.models import *
from django.contrib import messages
from django.db.models import Sum, Count
from datetime import datetime, date


# Create your views here.


def viewexpense(request):
    allregularmonthlyexpense = regularmonthlyexpense.objects.all().order_by(
        'expenseAmount').reverse()
    allregularmonthlysavings = regularmonthlysavings.objects.all()
    allunexpectedmonthlyexpense = unexpectedmonthlyexpense.objects.all()
    allregularmonthlyincome = regularmonthlyincome.objects.all()

    totalRegularExpense = regularmonthlyexpense.objects.aggregate(
        Sum('expenseAmount'))['expenseAmount__sum']
    totalMonthlyIncome = regularmonthlyincome.objects.aggregate(
        Sum('incomeAmount'))['incomeAmount__sum']
    totalSavings = regularmonthlysavings.objects.all().aggregate(
        Sum('savingsAmount'))['savingsAmount__sum']
    totalMonthlySavings = totalSavings
    totalUnexpectedExpense = unexpectedmonthlyexpense.objects.all().exclude(
        expenseStatus=False).aggregate(
        Sum('expenseAmount'))['expenseAmount__sum']

    totalUnexpectedExpense = 0.00 if totalUnexpectedExpense is None else totalUnexpectedExpense

    totalSavings = (totalSavings/totalMonthlyIncome) * 100
    expensePercentage = (totalRegularExpense/totalMonthlyIncome) * 100
    leftOverPercentage = ((totalMonthlyIncome -
                          (totalSavings+totalRegularExpense)) / totalMonthlyIncome) * 100

    return render(request, "viewexpense.html", {"allregularmonthlyexpense": allregularmonthlyexpense, "allunexpectedmonthlyexpense":
                                                allunexpectedmonthlyexpense, "allregularmonthlyincome": allregularmonthlyincome,
                                                "totalRegularExpense": totalRegularExpense, "totalMonthlyIncome": totalMonthlyIncome,
                                                "expensePercentage": expensePercentage, "totalSavings": totalSavings, "allregularmonthlysavings": allregularmonthlysavings,
                                                "leftOverPercentage": leftOverPercentage, "totalUnexpectedExpense": totalUnexpectedExpense, "totalMonthlySavings": totalMonthlySavings})


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
    messages.success(
        request, 'Successfully removed the Unexpected Expense Item.')
    return redirect("viewexpense")


def editmonthlyexpense(request, item_id):
    edited_object = get_object_or_404(regularmonthlyexpense, pk=item_id)

    if request.method == 'POST':
        html_date_str = date.today().strftime('%Y-%m-%d') if (request.POST.get('expenseDate') ==
                                                              "") or (request.POST.get('expenseDate') is None) else request.POST.get('expenseDate')
        edited_object.expenseName = request.POST['expenseName']
        edited_object.expenseAmount = request.POST['expenseAmount']
        edited_object.expenseDate = datetime.strptime(
            html_date_str, '%Y-%m-%d').date()

        edited_object.save()
        format_message = "Successfully edited the Monthly Expense Item {}".format(
            edited_object.expenseName)
        messages.success(request, format_message)
        return redirect("viewexpense")
    else:
        return render(request, "editmonthlyexpense.html", {"edited_object": edited_object})
