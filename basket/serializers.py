from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from products.serializers import *
User = get_user_model()


class productIdSer(serializers.Serializer):
    product = serializers.IntegerField()


class rentedSerializer(serializers.ModelSerializer):
    product = getProductSerializer()
    class Meta:
        model = Rented
        fields = "__all__"
        read_only_fields = ("rented_day", "user")

class CreaterentedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rented
        fields = "__all__"
        read_only_fields = ("rented_day", "user")


class RentedActionSerializer(serializers.Serializer):
    action = serializers.CharField()
    id=serializers.IntegerField()