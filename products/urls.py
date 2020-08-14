from django.urls import path, include
from .views import *

urlpatterns = [
    path("create", product.as_view()),
    path('filter', getProduct.as_view({'get': 'list'})),

    path("favorites/<id>", product.as_view())
]