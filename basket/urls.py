from django.urls import path, include
from .views import *

urlpatterns = [
    path("rent", rentedApi.as_view()),
    path("", BasketView.as_view()),

    path("myRented", MyRentedProduct.as_view()),

    path("admin/get/new", adminNewRentedApi.as_view()),
    path("admin/get", adminRentedApi.as_view()),
    path("rent/action", AcceptOrRejectRent.as_view()),
    path("pickUp", DeliverToPickUp.as_view()),

    path("inStock", inStock.as_view()),

    path("deliver", deliver.as_view()),
    path("deliver/push", ToDeliverDate.as_view())
]