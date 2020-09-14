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
from message.models import Message
from utils.messages import *


class BasketView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = request.user.basket.all()
        s = getProductSerializer(queryset, many=True, context={'request': request})
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
        serializer_class = rentedSerializer(queryset, many=True, context={'request': request})
        for i in serializer_class.data:
            rented = datetime.strptime(i['rented_day'], '%Y-%m-%d')
            for j in i['product']:
                deadline = rented + timedelta(j['count_day'])
                if datetime.now() < deadline:
                    days_left = datetime.now()-deadline
                    # print(abs(days_left.days))
                    j['days_left'] = abs(days_left.days)
                else:
                    j['days_left'] = "deadline"
        return Response(serializer_class.data)

    def post(self, request):
        s = CreaterentedSerializer(data=request.data)
        if s.is_valid():
            print(s.validated_data)
            p = s.validated_data['products']
            get_product = s.validated_data['get_product']
            return_product = s.validated_data['return_product']
            amount = s.validated_data['amount']
            get_address = s.validated_data.get("get_address", None)
            return_address = s.validated_data.get("return_address", None)

            r = Rented.objects.create(
                user = request.user,
                get_product = get_product,
                return_product = return_product,
                return_address = return_address,
                get_address = get_address,
                amount = amount,
                is_checked = True
            )
            for i in p:
                p = Product.objects.get(id=i['id'])
                p.count_day = i['count_day']
                p.is_rented = True
                p.save()
                r.product.add(p)
                r.save()
                Message.objects.create(
                    user = p.owner,
                    text = deliverthenpickup(p.title),
                    ownerorclient = 1,
                    action = 3,
                    product = p,
                    get_or_return = 1,
                    order = r
                )
            if r.get_product == 1:
                Message.objects.create(
                    user = r.user,
                    text = deliverOne(r.id, r.product.all(), r.get_address, r.user.phone, r.get_product, r.return_product, r.amount),
                    action = 1,
                    order = r
                )
            else:
                Message.objects.create(
                    user = r.user,
                    text = PickupOne(r.id, r.product.all(), r.user.phone),
                    action = 1,
                    order = r
                )
            request.user.basket.clear()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class MyRentedProduct(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        products = Product.objects.filter(owner=request.user)
        for i in products:
            print(i.rented_obj.all())
        s = getProductSerializer(products, many=True, context={'request': request})
        # for i in serializer.data:
        #     deadline = datetime.strptime(i['deadline'], '%Y.%m.%d')
        #     if datetime.now() < deadline:
        #         days_left = datetime.now()-deadline
        #         # print(abs(days_left.days))
        #         i['days_left'] = abs(days_left.days)
        #     else:
        #         i['days_left'] = "deadline"
        return Response(s.data)


# from .tasks import send_notifiction
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
                # r.deadline = datetime.now() + timedelta(r.count_day)
                r.save()
                for i in r.product.all():
                    i.in_stock = False
                    i.leave = False
                    i.pickup = False
                    i.get_date = None
                    i.return_date = None
                    i.save()
            elif action == "end":
                r.is_ended = True
                r.save()
                for i in r.product.all():
                    i.in_stock = True
                    i.is_rented = False
                    i.save()
                    Message.objects.create(
                        user = i.owner,
                        get_or_return = 2,
                        action = 4,
                        ownerorclient = 1,
                        product = i,
                        order = r,
                        text = pickUPoint(i.title)
                    )
            return Response({'status': "ok"})
        else:
            return Response(s.errors)


class adminNewRentedApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Rented.objects.filter(is_rented=False, is_ended=False, is_checked=False)
        serializer_class = rentedSerializer(queryset, many=True, context={'request': request})
        return Response(serializer_class.data)

    def post(self, request):
        s = productIdSer(data=request.data)
        if s.is_valid():
            r = Rented.objects.get(id=s.validated_data['product'])
            r.is_checked = True
            r.save()
            for i in r.product.all():
                p = i
                p.is_rented = True
                p.save()
                Message.objects.create(
                    user = i.owner,
                    text = deliverthenpickup(i.title),
                    ownerorclient = 1,
                    action = 3,
                    product = i,
                    get_or_return = 1,
                    order = r
                )
            if r.get_product == 1:
                Message.objects.create(
                    user = r.user,
                    text = deliverOne(r.id, r.product.all(), r.get_address, r.user.phone),
                    action = 1,
                    order = r
                )
            else:
                Message.objects.create(
                    user = r.user,
                    text = PickupOne(r.id, r.product.all(), r.user.phone),
                    action = 1,
                    order = r
                )
            return Response({"status": "ok"})
        else:
            return Response(s.errors)


class adminRentedApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Rented.objects.filter(is_rented=True, is_ended=False, is_checked=True)
        serializer_class = rentedSerializer(queryset, many=True, context={'request': request})
        for i in serializer_class.data:
            rented = datetime.strptime(i['rented_day'], '%Y-%m-%d')
            for j in i['product']:
                deadline = rented + timedelta(j['count_day'])
                if datetime.now() < deadline:
                    days_left = datetime.now()-deadline
                    # print(abs(days_left.days))
                    j['days_left'] = abs(days_left.days)
                else:
                    j['days_left'] = "deadline"
        return Response(serializer_class.data)



class DeliverToPickUp(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Rented.objects.filter(is_rented=False, is_ended=False, is_checked=True)
        serializer_class = rentedSerializer(queryset, many=True, context={'request': request})
        return Response(serializer_class.data)

    # 
    def post(self, request):
        s = productIdSer(data=request.data)
        if s.is_valid():
            r = Rented.objects.get(id=s.validated_data['product'])
            for i in r.product.all():
                Message.objects.create(
                    user = i.owner,
                    text = deliverthenpickup(i.title),
                    ownerorclient = 1,
                    action = 2,
                    product = i,
                    get_or_return = 1,
                    order = r
                )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class inStock(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = productIdSer(data=request.data)
        if s.is_valid():
            r = Product.objects.get(id=s.validated_data['product'])
            r.in_stock = True
            r.save()
            # order = r.rented_obj.all()[1]
            # c = False
            # for j in order.product.all():
            #     if j.in_stock == True:
            #         c = True
            #     else:
            #         c = False
            #         break
            # if c:
            #     if order.get_product == 1:
            #         Message.objects.create(
            #             user = order.user,
            #             text = deliverTwo(order.id),
            #             order = order,
            #             get_or_return = 1,
            #             action = 2,
            #             ownerorclient = 2
            #         )
            #     else:
            #         Message.objects.create(
            #             user = order.user,
            #             text = PickupTwo(order.id),
            #             order = order,
            #             get_or_return = 1,
            #             action = 1,
            #             ownerorclient = 2
            #         )   
            return Response({'status': "ok"})
        else:
            return Response(s.errors)



class ToDeliverDate(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = OrderidSer(data = request.data)
        if s.is_valid():
            o = Rented.objects.get(id = s.validated_data['order_id'])
            if o.get_product == 1:
                Message.objects.create(
                    user = o.user,
                    text = deliverTwo(o.id),
                    order = o,
                    get_or_return = 1,
                    action = 2,
                    ownerorclient = 2
                )
            else:
                Message.objects.create(
                    user = o.user,
                    text = PickupTwo(o.id),
                    order = o,
                    action = 1,
                    get_or_return = 1,
                    ownerorclient = 2
                )                
            return Response({"status": "ok"})
        else:
            return Response(s.errors)


class deliver(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        r = Rented.objects.filter(is_rented=False)
        print(r)
        a = []
        for i in r:
            c = False
            for j in i.product.all():
                if j.in_stock == True:
                    c = True
                else:
                    c = False
                    break
            if c:
                a.append(i)
        s = rentedSerializer(a, many=True, context={'request': request})
        return Response(s.data)

