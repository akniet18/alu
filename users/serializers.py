from rest_framework import serializers
from .models import *


class PhoneS(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    name = serializers.CharField(required=False)

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField()


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("avatar",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("avatar","nickname", "phone")
        read_only_fields = ("avatar", "phone")
