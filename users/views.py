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
from products.models import *
from utils.compress import *
from push_notifications.models import APNSDevice, GCMDevice
from utils.push import send_push
from utils.smsc_api import SMSC
# from django_auto_prefetching import AutoPrefetchViewSetMixin
smsc = SMSC()



class PhoneCode(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = PhoneS(data=request.data)
        rand = random.randint(1000, 9999)
        if s.is_valid():
            nickname = s.validated_data['name']
            phone = s.validated_data['phone']
            if phone[0] != "+":
                phone = "+" + phone
            if PhoneOTP.objects.filter(phone = phone).exists():
                a = PhoneOTP.objects.get(phone = phone)
                a.nickname = nickname
                if phone == "+77783579279":
                    a.otp = "1111"
                else:
                    a.otp = rand
                # a.otp = "1111"
                a.save()
            else:
                if phone == "+77783579279":
                    PhoneOTP.objects.create(phone=phone, otp="1111", nickname=nickname)
                else:
                    PhoneOTP.objects.create(phone=phone, otp=str(rand), nickname=nickname)
                    # PhoneOTP.objects.create(phone=phone, nickname=nickname, otp=str(1111))
                if phone != "+77783579279":
                    smsc.send_sms(phone, "Ваш код ALU: "+str(rand), sender="sms")
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
                nickname = u.nickname
                # u.save()
                if User.objects.filter(phone=phone).exists():
                    us = User.objects.get(phone=phone)
                    uid = us.pk
                    us.nickname = nickname
                    us.save()
                else:
                    us = User.objects.create(phone=phone, nickname=nickname)
                    uid = us.pk
                if Token.objects.filter(user=us).exists():
                    token = Token.objects.get(user=us)
                else:
                    token = Token.objects.create(user=us)
                # user = authenticate(phone=phone)
                # django_login(request, us)
                return Response({'key': token.key, 'uid': uid, 'status': 'ok', 'nickname': us.nickname})
            else:
                return Response({'status': 'otp error'})
        else:
            return Response(s.errors)


class LoginUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        s = PhoneS(data=request.data)
        if s.is_valid():
            rand = random.randint(1000, 9999)
            phone = s.validated_data['phone']
            if phone[0] != "+":
                phone = "+" + phone
            user=User.objects.filter(phone=phone)
            if user.exists():
                if PhoneOTP.objects.filter(phone = phone).exists():
                    a = PhoneOTP.objects.get(phone = phone)
                    if phone == "+77783579279":
                        a.otp = "1111"
                    else:
                        a.otp = rand
                    a.save()
                else:
                    if phone == "+77783579279":
                        PhoneOTP.objects.create(phone=phone, otp="1111")
                    else:
                        PhoneOTP.objects.create(phone=phone, otp=str(rand))
                if phone != "+77783579279":
                    smsc.send_sms(phone, "Ваш код ALU: "+str(rand), sender="sms")
                return Response({'status': "ok"})
            else:
                return Response({'status': 'not found'})
        else:
            return Response(s.errors)


class Logined(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            phone = s.validated_data['phone']
            if phone[0] != "+":
                phone = "+" + phone
            u = PhoneOTP.objects.get(phone=phone)
            if u.otp == str(s.validated_data['code']):
                us = User.objects.get(phone=phone) 
                if Token.objects.filter(user=us).exists():
                    token = Token.objects.get(user=us)
                else:
                    token = Token.objects.create(user=us)
                return Response({'key': token.key, 'uid': us.id, 'status': 'ok', 'nickname': us.nickname})
            else:
                return Response({'status': 'otp error'})
        else:
            return Response(s.errors)


class Avatar(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = AvatarSerializer(data=request.data)
        if s.is_valid():
            ava = s.validated_data['avatar']
            img = base64img(ava, 'avatar')
            avatar = compress_image(img, (200, 200))
            request.user.avatar = avatar
            request.user.save()
            return Response({'status': "ok", "avatar": request.user.avatar.url})
        else:
            return Response(s.errors)


class detailUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        u = User.objects.get(id = id)
        s = UserSerializer(u, context={'request': request})
        return Response(s.data)

    def post(self, request, id):
        s = UserSerializer(data=request.data)
        if s.is_valid():
            u = User.objects.get(id = id)
            u.nickname = s.validated_data['nickname']
            u.save()
            return Response({'status': "ok"})
        else:
            return Response(s.errors)



class login_admin(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = LoginAdminSerializer(data=request.data)
        if s.is_valid():
            phone = s.validated_data['phone']
            password = s.validated_data['password']
            if User.objects.filter(phone=phone, is_staff=True).exists():
                us = User.objects.get(phone=phone)
                if us.check_password(password):
                    us = us
                else:
                    return Response({'status': 'error'})
            else:
                return Response({'status': 'error'})
            if Token.objects.filter(user=us).exists():
                token = Token.objects.get(user=us)
            else:
                token = Token.objects.create(user=us)
            # django_login(request, us)
            return Response({'key': token.key, 'uid': us.pk})
        else:
            return Response(s.errors)


class admin_side_get_view(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user
        if user.role == User.ROLE_SALES_DEPARTMENT:
            p = Product.object.filter(category__isnull = True)
        elif user.role == User.ROLE_CONTROL_DEPARTMENT:
            p = Product.object.filter(category__isnull = True)



class pushRegister(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        s = pushSerializer(data=request.data)
        if s.is_valid():
            cmt = s.validated_data['cmt']
            if cmt == "apn":
                APNSDevice.objects.get_or_create(user = request.user, 
                                        defaults={'registration_id': s.validated_data['reg_id']})
            else:
                GCMDevice.objects.get_or_create(user=request.user, active=True,
                                        defaults={'registration_id': s.validated_data['reg_id']},
                                        cloud_message_type="FCM")
            return Response({'status': "ok"})
        else:
            return Response(s.errors)


def privatepolicy(request):
    context = {'context': ""}
    return render(request, 'index.html', context)


class SendPush(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        user = User.objects.get(id=1)
        print(user)
        send_push(user, "Здравствуйте! Вами оформлен заказ №12345 Планируемый срок формирования заказа — от 1 до 3 дней Уведомления обо всех изменениях заказа и даты комплектации товаров Вы получите в разделе 'Сообщения'. Заказанные товары: Книга 'Растворится в воздухе' - 1 300 тг на 30 дней Книга 'осле меня' - 2 300 тг на 60 дней Метод доставки: Курьерская доставка стоимость доставки: 800 тг. Адрес доставки: ул. Тимирязева 26 (значение из заполненного поля доставка) Итого: 6500 тг Контактный номер, (значение номера при регистрации на платформе) Благодарим Вас за то, что Вы выбрали нашу платформу ALU.KZ! Мы рады, что Вы являетесь нашим клиентом. Если у Вас возникнут вопросы, пожалуйста, обращайтесь к нам.")
        return Response({'starus': "ok"})