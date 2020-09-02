from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(serializers.Serializer):
    phones = serializers.ListField(child = serializers.CharField())
    product_image = serializers.ListField(child=serializers.ImageField())
    title = serializers.CharField()
    price = serializers.IntegerField()
    # city = 
    address = serializers.CharField()
    

class getProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'subcategory', 'subcategory2')