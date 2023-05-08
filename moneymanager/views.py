from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import moneymanager
from .forms import MoneyForm
import requests
from django.contrib import messages
from datetime import datetime, date
from django.db.models import F, DecimalField, ExpressionWrapper, Sum, Count

# Create your views here.


def viewmoney(request):
    allmoneyitems = moneymanager.objects.all()
    totalCash = 0
    inr_amount = 0
    totalAmounts = moneymanager.objects.values('cashType').order_by(
        'cashType').annotate(totalCashAmount=Sum('cashAmount'))

    for eachCashItem in allmoneyitems:
        totalCash = totalCash + eachCashItem.cashAmount

    forex_url = f'https://v6.exchangerate-api.com/v6/beeb6efe4b832b73f5f8911e/pair/USD/INR/{totalCash}'
    response = requests.get(forex_url)
    forex_data = response.json()
    conversion_rate = Decimal(forex_data["conversion_rate"])
    conversion_rate = format(conversion_rate, ".2f")
    inr_amount = Decimal(forex_data["conversion_result"])
    allmoneyitems = moneymanager.objects.annotate(
        percentageInvolved=ExpressionWrapper(
            F("cashAmount") / totalCash * 100, output_field=DecimalField()
        )
    )
    for eachCashItem in allmoneyitems:
        eachCashItem.percentageInvolved = eachCashItem.cashAmount / totalCash * 100
    format_message = "Current USD to INR Rate is:- {}".format(conversion_rate)
    messages.success(
        request, format_message)
    return render(request, "viewmoney.html", {"allmoneyitems": allmoneyitems, "totalCash": totalCash, "inr_amount": inr_amount, "currentRate": Decimal(forex_data["conversion_rate"]), "totalAmounts": totalAmounts})


def addmoney(request):
    CashType = ["Certificate of Deposit",
                "Savings", "Checking", "T Bills", "I Bonds"]
    if request.method == "POST":
        form = MoneyForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Successfully added money item to your list.')
            return redirect("viewmoney")
    else:
        return render(request, "addmoney.html", {"cashdata": CashType})


def editmoney(request, item_id):
    CashType = ["Certificate of Deposit",
                "Savings", "Checking", "T Bills", "I Bonds"]
    modified_object = get_object_or_404(moneymanager, pk=item_id)

    if request.method == 'POST':
        cashName = modified_object.cashName if (request.POST.get('cashName') == "") or (
            request.POST.get('cashName') is None) else request.POST.get('cashName')
        cashType = modified_object.cashType if (request.POST.get('cashType') == "") or (
            request.POST.get('cashType') is None) else request.POST.get('cashType')
        cashAmount = modified_object.cashAmount if (request.POST.get('cashAmount') == "") or (
            request.POST.get('cashAmount') is None) else request.POST.get('cashAmount')
        cashRate = modified_object.cashRate if (request.POST.get('cashRate') == "") or (
            request.POST.get('cashRate') is None) else request.POST.get('cashRate')

        cashMaturityDate = modified_object.cashMaturityDate.strftime('%Y-%m-%d') if (request.POST.get('cashMaturityDate') ==
                                                                                     "") or (request.POST.get('cashMaturityDate') is None) else request.POST.get('cashMaturityDate')
        cashStartDate = modified_object.cashStartDate.strftime('%Y-%m-%d') if (request.POST.get('cashStartDate') ==
                                                                               "") or (request.POST.get('cashStartDate') is None) else request.POST.get('cashStartDate')

        modified_object.cashName = cashName
        modified_object.cashType = cashType
        modified_object.cashAmount = cashAmount
        modified_object.cashRate = cashRate
        modified_object.cashStartDate = cashStartDate
        modified_object.cashMaturityDate = cashMaturityDate

        modified_object.save()
        format_message = "Successfully edited the Money Item {}".format(
            modified_object.cashName)
        messages.success(request, format_message)
        return redirect("viewmoney")
    else:
        format_message = "You are editing - {}".format(
            modified_object.cashName)
        messages.success(request, format_message)
        return render(request, "editmoney.html", {"editobject": modified_object, "cashdata": CashType})
