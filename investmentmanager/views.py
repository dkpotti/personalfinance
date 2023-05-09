from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Sum, Count
from django.contrib import messages
import requests
from decimal import Decimal


# Create your views here.


def viewinvestment(request):
    allmonthlyinvestments = monthlyinvestment.objects.all().order_by(
        'investmentConverted').reverse()
    totalMonthlyInvestment = Decimal(0)
    for eachInvestment in allmonthlyinvestments:
        forex_url = f'https://v6.exchangerate-api.com/v6/beeb6efe4b832b73f5f8911e/pair/{eachInvestment.investmentCurrency}/USD/{eachInvestment.investmentAmount}'
        response = requests.get(forex_url)
        forex_data = response.json()
        totalMonthlyInvestment = totalMonthlyInvestment + \
            Decimal(forex_data["conversion_result"])
        conversion_rate = Decimal(forex_data["conversion_result"])
        conversion_rate = format(conversion_rate, ".2f")
        eachInvestment.investmentConverted = conversion_rate
        eachInvestment.save()

    # totalMonthlyInvestment = allmonthlyinvestments.objects.aggregate(
    #     Sum('investmentConverted'))['investmentConverted__sum']

    return render(request, "viewinvestment.html", {"allmonthlyinvestments": allmonthlyinvestments, "totalMonthlyInvestment": totalMonthlyInvestment})


def addmonthlyinvestment(request):
    if request.method == "POST":
        form = MonthlyInvestmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("viewinvestment")

    else:
        return render(request, "addmonthlyinvestment.html", {})


def editmonthlyinvestment(request, item_id):
    modified_object = get_object_or_404(monthlyinvestment, pk=item_id)
    if request.method == 'POST':
        modified_object.investmentName = request.POST['investmentName']
        modified_object.investmentAmount = request.POST['investmentAmount']
        modified_object.investmentDate = request.POST['investmentDate']
        modified_object.save()
        messages.success(request, 'Successfully edited the Investment Item.')
        return redirect("viewinvestment")
    else:
        return render(request, "editinvestment.html", {"modified_object": modified_object})
