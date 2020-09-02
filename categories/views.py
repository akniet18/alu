from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import random
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import viewsets, generics, permissions
from datetime import datetime
from products.models import *



class addCategory(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, id):
        s = addCategorySerializer(data=request.data)
        if s.is_valid():
            p = Product.objects.get(id = id)
            p.category = s.validated_data['category']
            p.subcategory = s.validated_data['subcategory']
            p.subcategory2 = s.validated_data['subcategory2']
            p.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)



