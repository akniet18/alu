from rest_framework import serializers
from .models import *


class MessageSer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class PostMessageSer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField(required=False)
    action = serializers.IntegerField(required=False)