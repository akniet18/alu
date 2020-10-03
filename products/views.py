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
from utils.push import send_push


class getProduct(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    queryset = Product.objects.filter(is_publish=True)
    serializer_class = getProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ('title', 'about')
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
        r = Recomendation.objects.get(id=1).products.all()
        ids = []
        for i in r:
            ids.append(i.id)
        queryset = Product.objects.filter(is_publish=True).exclude(id__in=ids).order_by("-publish_date")[:50]
        queryset = list(r)+list(queryset)
        serializer_class = getProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer_class.data)

    def post(self, request):
        s = productIdSer(data=request.data)
        if s.is_valid():
            product = Product.objects.get(id=s.validated_data['product'])
            r, created = Recomendation.objects.get_or_create(id=1)
            if product in r.products.all():
                r.products.remove(product)
            else:
                r.products.add(product)
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)

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
                price_14_owner = price_14,
                price_30_owner = price_30,
                phones = phones,
                owner = request.user,
                location = location,
            )
            if images:
                for i, val in enumerate(images):
                    im = base64img(val, str(p.id)+str(i))
                    img = compress_image(im, (400, 400))
                    ProductImage.objects.create(
                        product = p,
                        image = img
                    )
            return Response({'status': "ok"}) 
        else:
            return Response(s.errors)


class Delete(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = productIdSer(data = request.data)
        if s.is_valid():
            p = Product.objects.get(id=s.validated_data['product']).delete()
            return Response({'status': 'ok'})
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


class ProductChange(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = ProductChangeSer(data = request.data)
        if s.is_valid():
            p = Product.objects.get(id=s.validated_data['id'])
            price_14 = s.validated_data.get("price_14", None)
            price_30 = s.validated_data.get("price_30", None)
            about = s.validated_data.get("about", None)
            title = s.validated_data.get("title", None)
            if price_14:
                p.price_14 = price_14
            if price_30:
                p.price_30 = price_30
            if about:
                p.about = about
            if title:
                p.title = title
            p.save()
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
            m = Message.objects.create(
                user = product.owner,
                action = 1,
                text = product_publish(product.title),
                words = [product.title]
            )
            send_push(product.owner, push1())
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
        p = Product.objects.filter(is_rented=True, count_day__isnull=False, rented_obj__is_rented=True,
                                    rented_obj__return_product=1, rented_obj__is_ended=False)
        a = []
        for i in p:
            rented_ob = None
            for s in i.rented_obj.all():
                if s.is_ended == False:
                    rented_ob = s
            rented = datetime.strptime(str(rented_ob.rented_day), '%Y-%m-%d')
            deadline = rented + timedelta(i.count_day)
            days_left = datetime.now()-deadline
            days_left = int(days_left.total_seconds()) // (24 * 3600)
            print(days_left)
            if days_left >= -1:
                if days_left == -1:
                    i.days_left = 1
                elif days_left == 0:
                    i.days_left = 1
                else:
                    i.days_left = "-{}".format(days_left)
                i.return_date = rented_ob.return_date
                a.append(i)
        s = getProductSerializer2(a, many=True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = productIdSer(data = request.data)
        if s.is_valid():
            p = Product.objects.get(id=s.validated_data['product'])
            p.is_rented = False
            p.count_day = None
            p.get_date = None
            p.in_stock = True
            p.return_date = None
            p.save()
            r = p.rented_obj.all()[0]
            r.is_ended = True
            r.save()
            m1 = Message.objects.create(
                user = p.owner,
                get_or_return = 2,
                action = 4,
                ownerorclient = 1,
                product = p,
                order = r,
                text = pickUPoint(p.title),
                words = [p.title]
            )
            m2 = Message.objects.create(
                user = p.owner,
                action = 1,
                product = p,
                text = product_publish(p.title),
                words = [p.title]
            )
            send_push(p.owner, push3())
            send_push(p.owner, push1())
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class RetrunPickup(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        p = Product.objects.filter(is_rented=True, count_day__isnull=False, rented_obj__is_rented=True, 
                                rented_obj__return_product=2, rented_obj__is_ended=False)
        a = []
        for i in p:
            rented_ob = None
            for s in i.rented_obj.all():
                if s.is_ended == False:
                    rented_ob = s
            rented = datetime.strptime(str(rented_ob.rented_day), '%Y-%m-%d')
            deadline = rented + timedelta(i.count_day)
            days_left = datetime.now()-deadline
            days_left = int(days_left.total_seconds()) // (24 * 3600)
            print(days_left)
            if days_left >= -1:
                if days_left == -1:
                    i.days_left = 1
                elif days_left == 0:
                    i.days_left = 1
                else:
                    i.days_left = "-{}".format(days_left)
                i.return_date = rented_ob.return_date
                a.append(i)
            
        s = getProductSerializer2(a, many=True, context={'request': request})
        return Response(s.data)


class ReturnProduct(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Product.objects.filter(in_stock=True, is_rented=False, leave=False)
        s = getProductSerializer(queryset, many=True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = productIdSer(data = request.data)
        if s.is_valid():
            p = Product.objects.get(id=s.validated_data['product'])
            p.in_stock = False
            p.get_date = None
            p.return_date = None
            p.leave = False
            p.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class productInStock(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Product.objects.filter(in_stock=True, is_rented=False, leave=True)
        s = getProductSerializer(queryset, many=True, context={'request': request})
        return Response(s.data)

