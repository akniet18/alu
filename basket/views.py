from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import random
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import viewsets, generics, permissions
from datetime import datetime, timedelta
from products.models import *
from products.serializers import *



class BasketView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = request.user.basket.all()
        s = getProductSerializer(queryset, many=True)
        return Response(s.data)
    
    def post(self, request):
        s = productIdSer(data=request.data)
        if s.is_valid():
            product = Product.objects.get(id=s.validated_data['product'])
            if product in request.user.basket.all():
                request.user.basket.remove(product)
            else:
                request.user.basket.add(product)
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)
            


class rentedApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Rented.objects.filter(user=request.user, is_rented=True, is_ended=False)
        serializer_class = rentedSerializer(queryset, many=True)
        for i in serializer_class.data:
            deadline = datetime.strptime(i['deadline'], '%Y-%m-%d')
            if datetime.now() < deadline:
                days_left = datetime.now()-deadline
                # print(abs(days_left.days))
                i['days_left'] = abs(days_left.days)
            else:
                i['days_left'] = "deadline"
        return Response(serializer_class.data)

    def post(self, request):
        s = CreaterentedSerializer(data=request.data)
        if s.is_valid():
            print(s.validated_data)
            p = s.validated_data['product']
            count_day = s.validated_data['count_day']
            get_product = s.validated_data['get_product']
            return_product = s.validated_data['return_product']
            get_address = s.validated_data.get("get_address", None)
            return_address = s.validated_data.get("return_address", None)
            
            Rented.objects.create(
                product = p,
                user = request.user,
                count_day = count_day,
                get_product = get_product,
                return_product = return_product,
                return_address = return_address,
                get_address = get_address
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class MyRentedProduct(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        products = Rented.objects.filter(product__owner=request.user, is_rented=True, is_ended=False)
        serializer = rentedSerializer(products, many=True)
        for i in serializer.data:
            deadline = datetime.strptime(i['deadline'], '%Y.%m.%d')
            if datetime.now() < deadline:
                days_left = datetime.now()-deadline
                # print(abs(days_left.days))
                i['days_left'] = abs(days_left.days)
            else:
                i['days_left'] = "deadline"
        return Response(serializer.data)



class AcceptOrRejectRent(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = RentedActionSerializer(data=request.data)
        if s.is_valid():
            action = s.validated_data['action']
            r = Rented.objects.get(id=s.validated_data['id'])
            if action == "accept":
                r.is_rented = True
                r.rented_day = datetime.now()
                r.deadline = datetime.now() + timedelta(r.count_day)
                r.save()
            elif action == "return":
                r.is_ended = True
                r.save()
                p = r.product
                p.is_rented = False
                p.save()
            return Response({'status': "ok"})
        else:
            return Response(s.errors)


class adminNewRentedApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Rented.objects.filter(is_rented=False, is_ended=False, is_checked=False)
        serializer_class = rentedSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        s = productIdSer(data=request.data)
        if s.is_valid():
            r = Rented.objects.get(id=s.validated_data['product'])
            r.is_checked = True
            r.save()
            p = r.product
            p.is_rented = True
            p.save()
            return Response({"status": "ok"})
        else:
            return Response(s.errors)


class adminRentedApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Rented.objects.filter(is_rented=True, is_ended=False, is_checked=True)
        serializer_class = rentedSerializer(queryset, many=True)
        for i in serializer_class.data:
            deadline = datetime.strptime(i['deadline'], '%Y-%m-%d')
            if datetime.now() < deadline:
                days_left = datetime.now()-deadline
                # print(abs(days_left.days))
                i['days_left'] = abs(days_left.days)
            else:
                i['days_left'] = "deadline"
        return Response(serializer_class.data)



class DeliverToPickUp(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Rented.objects.filter(is_rented=False, is_ended=False, is_checked=True)
        serializer_class = rentedSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        s = productIdSer(data=request.data)
        if s.is_valid():
            owner = Rented.objects.get(id=s.validated_data['product']).product.owner
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class setDateToPickUp(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = setDateSer(data=request.data)
        if s.is_valid():
            r = Rented.objects.get(id=s.validated_data['id'])
            r.get_date = s.validated_data['date']
            r.save()
            return Response({'status': "ok"})
        else:
            return Response(s.errors)