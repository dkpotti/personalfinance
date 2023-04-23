from django.shortcuts import render, redirect
from decimal import Decimal
from .models import moneymanager
from .forms import MoneyForm
import requests
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
    inr_amount = Decimal(forex_data["conversion_result"])
    allmoneyitems = moneymanager.objects.annotate(
        percentageInvolved=ExpressionWrapper(
            F("cashAmount") / totalCash * 100, output_field=DecimalField()
        )
    )
    for eachCashItem in allmoneyitems:
        eachCashItem.percentageInvolved = eachCashItem.cashAmount / totalCash * 100
    return render(request, "viewmoney.html", {"allmoneyitems": allmoneyitems, "totalCash": totalCash, "inr_amount": inr_amount, "currentRate": Decimal(forex_data["conversion_rate"]), "totalAmounts": totalAmounts})


def addmoney(request):
    CashType = ["Certificate of Deposit",
                "Savings", "Checking", "T Bills", "I Bonds"]
    if request.method == "POST":
        form = MoneyForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("viewmoney")
    else:
        return render(request, "addmoney.html", {"cashdata": CashType})
