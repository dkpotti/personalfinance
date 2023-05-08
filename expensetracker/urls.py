from django.urls import path
from . import views


urlpatterns = [
    path("viewexpense/", views.viewexpense, name="viewexpense"),
    path("addregularexpense/", views.addregularexpense, name="addregularexpense"),
    path("addunexpectedexpense/", views.addunexpectedexpense,
         name="addunexpectedexpense"),
    path("addregularincome/", views.addregularincome, name="addregularincome"),
    path("delete/<item_id>", views.removeunexpectedexpense,
         name="removeunexpectedexpense"),
    path("editmonthlyexpense/<item_id>", views.editmonthlyexpense,
         name="editmonthlyexpense"),
]
