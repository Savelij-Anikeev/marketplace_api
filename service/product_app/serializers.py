from rest_framework import serializers

from vendor_app.serializers import VendorSerializer
from .models import Product, Category, Sale

from static_app.serializers import ImageSerializer, VideoSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Used for `Category` model
    """
    class Meta:
        model = Category
        fields = ('id', 'name')


class SaleSerializer(serializers.ModelSerializer):
    """
    Used for `Sale` model
    """
    class Meta:
        model = Sale
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    General serializer for `Product` model
    """
    vendor = VendorSerializer(many=True)
    categories = CategorySerializer(many=True)
    sale = SaleSerializer()

    photos = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'cost', 'sale', 'final_cost',
                  'amount', 'slug', 'photos', 'videos',
                  'tags', 'vendor', 'categories', 'specs',)
        read_only_fields = ('vendor', 'slug', 'final_cost', )


class ProductListSerializer(serializers.ModelSerializer):
    """
    Used for GET requests for `Product` model
    """
    vendor = serializers.StringRelatedField(many=True)
    categories = serializers.StringRelatedField(many=True)
    sale = serializers.StringRelatedField(many=False)

    photos = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'cost', 'sale', 'final_cost',
                  'photos', 'videos', 'vendor', 'categories',)


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Used for POST requests for `Product` model
    """
    photos = serializers.ImageField()
    videos = serializers.FileField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'cost', 'sale', 'final_cost',
                  'amount', 'slug', 'photos', 'videos',
                  'tags', 'vendor', 'categories', 'specs',)
        read_only_fields = ('vendor', 'slug', 'final_cost', )


class ProductChangeSerializer(serializers.ModelSerializer):
    """
    Used for put/patch requests for `Product` model
    """
    photos = serializers.ImageField()
    videos = serializers.FileField()

    class Meta:
        model = Product
        fields = '__all__'



