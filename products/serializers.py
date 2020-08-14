from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    phones = serializers.ListField(child = serializers.CharField())
    product_image = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Product
        fields = ('title', 'price', 'phones', 'product_image')


class getProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'