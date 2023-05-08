from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Sum, Count
from django.contrib import messages
import requests
from decimal import Decimal
from datetime import datetime, date

# Create your views here.


def viewliabilities(request):
    allliabilities = liabilities.objects.all().order_by(
        'liabilityAmount').reverse()
    totalliabilitiesamount = liabilities.objects.exclude(liabilityStatus=False).aggregate(
        Sum('liabilityAmount'))['liabilityAmount__sum']
    totalliabilitiesamount = 0.00 if totalliabilitiesamount is None else totalliabilitiesamount
    return render(request, "viewliabilities.html", {"allliabilities": allliabilities, "totalliabilitiesamount": totalliabilitiesamount})


def addliability(request):
    if request.method == "POST":
        form = LiabilitiesForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("viewliabilities")
        else:
            return render(request, "addliability.html", {})
    else:
        return render(request, "addliability.html", {})


def editliability(request, item_id):
    edited_object = get_object_or_404(liabilities, pk=item_id)
    flag = True
    if request.method == 'POST':
        html_date_str = date.today().strftime('%Y-%m-%d') if (request.POST.get('liabilityDate') ==
                                                              "") or (request.POST.get('liabilityDate') is None) else request.POST.get('liabilityDate')
        edited_object.liabilityName = request.POST['liabilityName']
        edited_object.liabilityAmount = request.POST['liabilityAmount']
        edited_object.liabilityDate = datetime.strptime(
            html_date_str, '%Y-%m-%d').date()
        edited_object.liabilityTo = request.POST['liabilityTo']
        edited_object.liabilityStatus = bool(
            request.POST.get('liabilityStatus'))
        edited_object.save()
        messages.success(request, 'Successfully edited the Liability Item.')
        return redirect("viewliabilities")
    else:
        form = LiabilitiesForm()
        return render(request, "editliability.html", {"edited_object": edited_object})
