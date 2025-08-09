from rest_framework import serializers
from . import models
from django.utils.translation import gettext_lazy as _


class CategorySerializer(serializers.ModelSerializer):
    parent_read = serializers.StringRelatedField(source="parent")
    parent_write = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        source="parent",
        write_only=True
    )
    get_all_children_products = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = [
            'id',
            'name',
            'hierarchy',
            'parent_read',
            'parent_write',
            'get_all_children_products',
        ]
        read_only_fields = [
            'id',
            'hierarchy',
            'parent_read',
            'get_all_children_products',
        ]
    
    def get_get_all_children_products(self, obj):
        return obj.get_all_children_products()

    def validate(self, data):
        instance = self.instance or models.Category(**data)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.clean()
        return data


class DiscountSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=models.Product.objects.all(),
        many=True,
        allow_null=True
    )

    class Meta:
        model = models.Discount
        fields = [
            'id',
            'type',
            'amount',
            'start',
            'end',
            'products',
        ]
    
    def validate(self, data):
        instance = models.Discount(**data)
        if self.instance:
            instance.id = self.instance.id
        instance.clean()
        return data


class TagSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=models.Product.objects.all(),
        many=True,
        allow_null=True
    )

    class Meta:
        model = models.Tag
        fields = [
            'id',
            'name',
            'products',
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = "__all__"


class ImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        exclude = ['product',]


class ProductSerializer(serializers.ModelSerializer):

    # images: If you want to combine both read and write into one field, you can use a custom field with to_representation and to_internal_value.
    images_read = ImageReadSerializer(many=True, source="images")
    images_write = ImageSerializer(many=True, write_only=True, source="images")

    class Meta:
        model = models.Product
        fields = [
            'id',
            'title',
            'categoty',
            'main_image',
            'images_read',
            'images_write',
            'price',
            'discount',
            'tags',
            'description_brief',
            'description',
            'stock',
            # 'slug',
            'creation',
            'last_modification',
        ]
        read_only_fields = ['id', 'slug', 'creation', 'last_modification', 'images_read',]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(_("Price cannot be negative."))
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(_("Stock cannot be negative."))
        return value
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = models.Product.objects.create(**validated_data)
        for image_data in images_data:
            models.Image.objects.create(product=product, **image_data)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                models.Image.objects.create(product=instance, **image_data)
        return instance
