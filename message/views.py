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
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from locations.models import *
from basket.serializers import *


class MessageApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Message.objects.filter(user=request.user).order_by('-created')
        # ser = MessageSer(queryset, many=True)
        data = []
        for i in queryset:
            data.append({
                "id": i.id,
                "text": i.text,
                'action': i.action,
                'is_readed': i.is_readed,
                'created': i.created
            })
            if i.action == 1:
                i.is_readed = True
                i.save()
        return Response(data)

    def post(self, request):
        s = PostMessageSer(data = request.data)
        if s.is_valid():
            m = Message.objects.get(id=s.validated_data['id'])
            m.is_readed = True
            
            date = s.validated_data.get('date', None)
            leave = s.validated_data.get('leave', None)
            if date is not None:
                if m.ownerorclient == 1:
                    if m.get_or_return == 1:
                        m.product.get_date = date
                    else:
                        m.product.return_date = date
                    m.product.save()
                else:
                    if m.get_or_return == 1:
                        m.order.get_date = date
                    else:
                        m.order.return_date = date
                    m.order.save()
            # if leave:
            m.save()
            return Response({"status": "ok"})            
        else:
            return Response(s.errors)
        