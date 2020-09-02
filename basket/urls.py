from django.urls import path, include
from .views import *

urlpatterns = [
    path("rent", rentedApi.as_view()),
    path("", BasketView.as_view()),

    path("myRented", MyRentedProduct.as_view()),

    path("rent/action", AcceptOrRejectRent.as_view())
]