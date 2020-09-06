from django.urls import path, include
from .views import *

urlpatterns = [
    path("recomendation", recomendations.as_view()),
    path("create", product.as_view()),
    path('filter', getProduct.as_view({'get': 'list'})),

    path("favorites", favorites.as_view()),

    path('publish/<id>', ProductPublish.as_view()),
    # path('publish', ProductPublish.as_view()),

    path("admin/get", GetProductPublish.as_view()),
]