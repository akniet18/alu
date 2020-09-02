from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/<id>', addCategory.as_view())
]