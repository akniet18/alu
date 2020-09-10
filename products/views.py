from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import random
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework import viewsets, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveUpdateAPIView
from datetime import datetime
from utils.compress import *
from utils.messages import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from locations.models import *
from basket.serializers import *
from message.models import Message
from datetime import datetime, timedelta

class getProduct(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    queryset = Product.objects.filter(is_publish=True)
    serializer_class = getProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ('title',)
    filter_fields = ('category','subcategory', 'subcategory2', "price_14", "price_30")
    

    def get_queryset(self):
        # user = self.request.user
        # if user.is_authenticated:
        #     if user.role == 1:
        #         self.queryset = Product.objects.filter(is_publish=False)
        minheight = self.request.GET.get('minprice')
        maxheight = self.request.GET.get('maxprice')
        if(minheight and maxheight):
            return self.queryset.filter(price_14__gte=minheight, price_14__lte=maxheight)
        return self.queryset


class recomendations(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        queryset = Product.objects.filter(is_publish=True).order_by("-publish_date")
        serializer_class = getProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer_class.data)

   


# product create
class product(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        s = ProductSerializer(data = request.data)
        if s.is_valid():
            # print(s.validated_data)
            title = s.validated_data['title']
            about = s.validated_data['about']
            price_14 = s.validated_data['price_14']
            price_30 = s.validated_data['price_30']
            phones = s.validated_data['phones']
            images = s.validated_data.get('product_image', None)
            address1 = s.validated_data['address']
            city = City.objects.get(id=1)
            location, created = Location.objects.get_or_create(
                city = city,
                address = address1
            )
            p = Product.objects.create(
                title = title,
                about = about,
                price_14 = price_14,
                price_30 = price_30,
                phones = phones,
                owner = request.user,
                location = location,
            )
            if images:
                for i, val in enumerate(images):
                    im = base64img(val, str(p.id)+str(i))
                    img = compress_image(im, (200, 200))
                    ProductImage.objects.create(
                        product = p,
                        image = img
                    )
            return Response({'status': "ok"}) 
        else:
            return Response(s.errors)


class favorites(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = request.user.favorites.all()
        s = getProductSerializer(queryset, many = True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = productIdSer(data=request.data)
        if s.is_valid():
            product = Product.objects.get(id=s.validated_data['product'])
            if product in request.user.favorites.all():
                request.user.favorites.remove(product)
            else:
                request.user.favorites.add(product)
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class ProductPublish(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        s = ProductPublishSerializer(data=request.data)
        if s.is_valid():
            product = Product.objects.get(id=id)
            product.category = s.validated_data['category']
            product.subcategory = s.validated_data['subcategory']
            product.subcategory2 = s.validated_data['subcategory2']
            product.is_publish = True
            product.publish_date = datetime.now()
            product.save()
            Message.objects.create(
                user = product.owner,
                action = 1,
                text = product_publish(product.title)
            )
            return Response({"status": "ok"})
        else:
            return Response(s.errors)
            

class GetProductPublish(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        p = Product.objects.filter(is_publish=False)
        s = getProductSerializer(p, many=True, context={'request': request})
        return Response(s.data)



class ReturnApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        p = Product.objects.filter(is_rented=True, count_day__isnull=False, rented_obj__is_rented=True)
        a = []
        for i in p:
            rented = datetime.strptime(str(i.rented_obj.all()[0].rented_day), '%Y-%m-%d')
            deadline = rented + timedelta(i.count_day)
            if datetime.now() < deadline:
                days_left = datetime.now()-deadline
                # print(abs(days_left.days))
                if abs(days_left.days) == 1:
                    a.append(i)
            
        s = getProductSerializer(a, many=True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = productIdSer(data = request.data)
        if s.is_valid():
            p = Product.objects.get(id=s.validated_data['product'])
            p.is_rented = False
            p.count_day = None
            p.get_date = None
            p.save()
            r = p.rented_obj.all()[0]
            r.is_ended = True
            r.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


def send_push():
    p = Product.objects.filter(is_rented=True, count_day__isnull=False, rented_obj__is_rented=True)
    a = []
    for i in p:
        r = i.rented_obj.all()[0]
        rented = datetime.strptime(str(r.rented_day), '%Y-%m-%d')
        deadline = rented + timedelta(i.count_day)
        if datetime.now() < deadline:
            days_left = datetime.now()-deadline
            # print(abs(days_left.days))
            if abs(days_left.days) == 1:
                # a.append(i)
                if r.return_product == 1:
                    mid = Message.objects.create(
                        user = r.user,
                        text = deliverThree(i.title),
                        action = 2,
                        order = r,
                        product = i,
                        get_or_return = 2
                    )
                else:
                    mid = Message.objects.create(
                        user = r.user,
                        text = PickupThree(i.title),
                        action = 1,
                        order = r,
                        product = i,
                        get_or_return = 2
                    )
    return "ok"