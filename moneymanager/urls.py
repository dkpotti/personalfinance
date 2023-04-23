from django.urls import path
from . import views


urlpatterns = [
    path("viewmoney/", views.viewmoney, name="viewmoney"),
    path("addmoney/", views.addmoney, name="addmoney"),
]
