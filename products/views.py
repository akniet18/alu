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
from utils.compress import compress_image
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend



class getProduct(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    queryset = Product.objects.all()
    serializer_class = getProductSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('category','subcategory', 'subcategory2', "price")

    def get_queryset(self):
        minheight = self.request.GET.get('minprice')
        maxheight = self.request.GET.get('maxprice')
        if(minheight and maxheight):
            return self.queryset.filter(price__gte=minheight, price__lte=maxheight)
        return self.queryset


class product(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = ProductSerializer(data = request.data)
        if s.is_valid():
            # print(s.validated_data)
            title = s.validated_data['title']
            price = s.validated_data['price']
            phones = s.validated_data['phones']
            images = s.validated_data['product_image']
            p = Product.objects.create(
                title = title,
                price = price,
                phones = phones
            )
            for i in images:
                img = compress_image(i, (200, 200))
                ProductImage.objects.create(
                    product = p,
                    image = img
                )
            return Response({'status': "ok"})
        else:
            return Response(s.errors)


class favorites(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        product = Product.objects.get(id=id)
        if product in request.user.favorites.all():
            request.user.favorites.remove(product)
        else:
            request.user.favorites.add(product)
        return Response({'status': 'ok'})


