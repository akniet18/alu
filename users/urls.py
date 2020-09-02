from django.urls import path, include
from .views import *

urlpatterns = [
    path('phone/otp/', PhoneCode.as_view()),
    path('register/', Register.as_view()),

    path('phone/check', LoginUser.as_view()),
    path('login', Logined.as_view())
]