from django.urls import path, include
from .views import *

urlpatterns = [
    path("create", product.as_view()),
    path('filter', getProduct.as_view({'get': 'list'})),

    path("favorites", favorites.as_view()),

    path('publish/<id>', ProductPublish.as_view()),
    path('publish', ProductPublish.as_view())
]