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
        fields = "id, name, parent_read, parent_write"
    
    def validate(self, data):
        instance = models.Category(**data)
        if self.instance:
            instance.id = self.instance.id
        instance.clean()
        return data



class DiscountSerializer(serializers.ModelSerializer):
    pass
    


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Product
