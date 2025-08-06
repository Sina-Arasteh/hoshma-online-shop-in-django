from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    parent_read = serializers.StringRelatedField()
    parent_write = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        source="parent",
        write_only=True
    )

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'parent_read', 'parent_write', 'depth',]

    def validate(self, data):
        instance = models.Category(**data)
        if self.instance:
            instance.id = self.instance.id
        instance.clean()
        return data


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = "__all__"
    
    def validate(self, data):
        instance = models.Discount(**data)
        if self.instance:
            instance.id = self.instance.id
        instance.clean()
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = "__all__"
