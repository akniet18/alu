from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MessageApi.as_view())
]