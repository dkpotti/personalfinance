from django.urls import path
from . import views

urlpatterns = [
    path("viewinvestment/", views.viewinvestment, name="viewinvestment"),
    path("addmonthlyinvestment/", views.addmonthlyinvestment,
         name="addmonthlyinvestment"),
    path("editmonthlyinvestment/<item_id>",
         views.editmonthlyinvestment, name="editmonthlyinvestment"),

]
