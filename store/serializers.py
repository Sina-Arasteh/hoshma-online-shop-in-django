from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    class Meta:
        model = models.Category
        fields = "name, parent"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        
