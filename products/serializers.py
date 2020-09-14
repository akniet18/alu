from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from locations.serializers import *
User = get_user_model()
from users.serializers import UserSerializer

class ProductSerializer(serializers.Serializer):
    phones = serializers.ListField(child = serializers.CharField())
    product_image = serializers.ListField(child=serializers.CharField(), required=False)
    title = serializers.CharField()
    about = serializers.CharField()
    price_14 = serializers.IntegerField()
    price_30 = serializers.IntegerField()
    # city = 
    address = serializers.CharField()

class ProductImageSer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
    class Meta:
        model = ProductImage
        fields = "__all__"


class categorySer(serializers.Serializer):
    name = serializers.CharField()

class getProductSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    product_image = ProductImageSer(many=True)
    subcategory = categorySer()
    owner = UserSerializer()
    class Meta:
        model = Product
        fields = '__all__'


class getProductSerializer2(serializers.ModelSerializer):
    location = LocationSerializer()
    product_image = ProductImageSer(many=True)
    subcategory = categorySer()
    owner = UserSerializer()
    days_left = serializers.IntegerField()
    class Meta:
        model = Product
        fields = '__all__'


class ProductPublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'subcategory', 'subcategory2')


class ProductChangeSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    about = serializers.CharField(required=False)
    price_14 = serializers.IntegerField(required=False)
    price_30 = serializers.IntegerField(required=False)

