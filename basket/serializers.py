from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from products.serializers import *
from users.serializers import UserSerializer
User = get_user_model()


class productIdSer(serializers.Serializer):
    product = serializers.IntegerField()


class rentedSerializer(serializers.ModelSerializer):
    product = getProductSerializer(many=True)
    user = UserSerializer()
    class Meta:
        model = Rented
        fields = "__all__"
        read_only_fields = ("rented_day", "user")

class CreaterentedSerializer(serializers.Serializer):
    products = serializers.ListField()
    get_product = serializers.IntegerField()
    return_product = serializers.IntegerField()
    get_address = serializers.CharField(required=False)
    return_address = serializers.CharField(required=False)
    amount = serializers.IntegerField()


class RentedActionSerializer(serializers.Serializer):
    action = serializers.CharField()
    id=serializers.IntegerField()


class setDateSer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField()