from django.urls import path
from . import views


app_name = "ecommerce_api"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="store_home")
]
