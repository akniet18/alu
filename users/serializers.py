from rest_framework import serializers
from .models import *


class LoginAdminSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=15)


class PhoneS(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    name = serializers.CharField(required=False)

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField()


class AvatarSerializer(serializers.Serializer):
    avatar = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar_url')

    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.avatar.url)
    class Meta:
        model = User
        fields = ("id", "avatar", "nickname", "phone")
        read_only_fields = ("avatar", "phone", "id")


class pushSerializer(serializers.Serializer):
	reg_id = serializers.CharField()
	cmt = serializers.CharField()