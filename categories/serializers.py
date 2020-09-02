from rest_framework import serializers
from .models import *
from products.models import *





class addCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("category", "subcategory", "subcategory2")