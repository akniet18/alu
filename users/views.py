from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import random
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from django.contrib.auth import (login as django_login,
                                 logout as django_logout)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveUpdateAPIView
from datetime import datetime
# from django_auto_prefetching import AutoPrefetchViewSetMixin


class PhoneCode(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = PhoneS(data=request.data)
        rand = random.randint(1000, 9999)
        if s.is_valid():
            # nickname = s.validated_data['nickname']
            phone = s.validated_data['phone']
            if phone[0] != "+":
                phone = "+" + phone
            print('code generate: ',s.validated_data, rand)
            if PhoneOTP.objects.filter(phone = phone).exists():
                a = PhoneOTP.objects.get(phone = phone)
                # a.nickname = nickname
                a.otp = rand
                # a.otp = "1111"
                a.save()
            else:
                PhoneOTP.objects.create(phone=phone, otp=str(rand))
                # PhoneOTP.objects.create(phone=phone, nickname=nickname, otp=str(1111))
            # smsc.send_sms(s.validated_data['phone'], "Код подтверждения: "+str(rand) + " Fixup", sender="sms")
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class Register(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            print('register: ', s.validated_data['phone'], s.validated_data['code'])
            phone = s.validated_data['phone']
            if phone[0] != "+":
                phone = "+" + phone
            u = PhoneOTP.objects.get(phone=phone)
            if u.otp == str(s.validated_data['code']):
                # u.validated = True
                # nickname = otpModel.nickname
                # u.save()
                if User.objects.filter(phone=phone).exists():
                    us = User.objects.get(phone=phone)
                    uid = us.pk
                    # us.nickname = nickname
                    # us.save()
                else:
                    us = User.objects.create(phone=phone)
                    uid = us.pk
                if Token.objects.filter(user=us).exists():
                    token = Token.objects.get(user=us)
                else:
                    token = Token.objects.create(user=us)
                # user = authenticate(phone=phone)
                # django_login(request, us)
                return Response({'key': token.key, 'uid': uid, 'status': 'ok'})
            else:
                return Response({'status': 'otp error'})
        else:
            return Response(s.errors)