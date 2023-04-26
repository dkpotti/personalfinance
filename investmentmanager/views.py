from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Sum, Count


# Create your views here.


def viewinvestment(request):
    allmonthlyinvestments = monthlyinvestment.objects.all()

    totalMonthlyInvestment = monthlyinvestment.objects.aggregate(
        Sum('investmentAmount'))['investmentAmount__sum']

    print(totalMonthlyInvestment)
    return render(request, "viewinvestment.html", {"allmonthlyinvestments": allmonthlyinvestments, "totalMonthlyInvestment": totalMonthlyInvestment})


def addmonthlyinvestment(request):
    if request.method == "POST":
        form = MonthlyInvestmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("viewinvestment")

    else:
        return render(request, "addmonthlyinvestment.html", {})
