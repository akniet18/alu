from django.urls import path, include
from .views import *

urlpatterns = [
    path('phone/otp/', PhoneCode.as_view()),
    path('register/', Register.as_view()),

    path('phone/check', LoginUser.as_view()),
    path('login', Logined.as_view()),
    path("admin/login", login_admin.as_view()),

    path("detail/<id>", detailUser.as_view()),
    path('avatar', Avatar.as_view()),

    path("push", pushRegister.as_view()),

    path("private/policy", privatepolicy)
]