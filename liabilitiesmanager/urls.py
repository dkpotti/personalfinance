from django.urls import path
from . import views

urlpatterns = [
    path("viewliabilities/", views.viewliabilities, name="viewliabilities"),
    path("addliability/", views.addliability,
         name="addliability"),
    path("editliability/<item_id>",
         views.editliability, name="editliability"),
]
