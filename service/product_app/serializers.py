from rest_framework import serializers

from vendor_app.serializers import VendorSerializer
from .ProductService import ProductService
from .models import Product, Category, Sale

from static_app.serializers import ImageSerializer, VideoSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Used for `Category` model
    """
    # top_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'sub_category')

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['sub_category'] = CategorySerializer(many=True)
        return fields


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
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'rating', 'cost', 'sale', 'final_cost',
                  'amount', 'slug', 'images', 'videos',
                  'tags', 'vendor', 'categories', 'specs',)
        read_only_fields = ('vendor', 'slug', 'final_cost', )


class ProductListSerializer(serializers.ModelSerializer):
    """
    Used for GET requests for `Product` model
    """
    vendor = VendorSerializer(many=True)
    categories = CategorySerializer(many=True)
    sale = serializers.StringRelatedField(many=False)
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'rating', 'images', 'videos', 'cost', 'sale', 'final_cost',
                  'vendor', 'categories',)


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Used for POST requests for `Product` model
    """
    images = ImageSerializer(read_only=True, many=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    videos = VideoSerializer(read_only=True, many=True)
    uploaded_videos = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    # vendor = VendorSerializer(required=False, many=True)
    # categories = CategorySerializer(many=)
    # vendor = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'cost', 'sale', 'final_cost',
                  'amount', 'slug', 'uploaded_images', 'uploaded_videos',
                  'tags', 'vendor', 'categories', 'specs', 'images', 'videos')
        read_only_fields = ('slug', 'final_cost')

    def create(self, validated_data):
        uploaded_images, uploaded_videos = ProductService.check_static(validated_data)
        vendor = validated_data.pop('vendor')

        product = super().create(validated_data)

        ProductService.give_static(uploaded_images, uploaded_videos, product)
        product.vendor.set(vendor)
        product.save()

        return product


class ProductChangeSerializer(serializers.ModelSerializer):
    """
    Used for put/patch requests for `Product` model
    """

    class Meta:
        model = Product
        fields = '__all__'


class ProductCartSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    vendor = VendorSerializer(many=True)
    categories = CategorySerializer(many=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'cost', 'sale', 'final_cost',
                  'amount', 'slug', 'tags', 'vendor', 'categories', 'images')

    def get_images(self, obj):
        return ImageSerializer(obj.images.all()[0]).data
