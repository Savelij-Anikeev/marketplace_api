from rest_framework import serializers

from vendor_app.serializers import VendorSerializer
from .ProductService import ProductService
from .models import Product, Category, Sale

from static_app.serializers import ImageSerializer, VideoSerializer


# cats
class CategorySerializer(serializers.ModelSerializer):
    """
    Used for `Category` model
    """
    # top_category = serializers.SerializerMethodField()
    child = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'child')

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['sub_category'] = CategorySerializer(many=True, required=False)
        return fields

    def get_child(self, obj):
        return CategorySerializer(obj.get_children(), many=True).data


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


# sales
class SaleSerializer(serializers.ModelSerializer):
    """
    Used for `Sale` model
    """
    class Meta:
        model = Sale
        fields = '__all__'


# products
class ProductRelatedProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'images', 'amount')

    def get_images(self, obj):
        # return ImageSerializer(obj.images.all()[0]).data
        a = []
        # for i in obj.all():
        for i in obj.related_products.all():
            a.append(i.images.all()[0])
        return a


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    General serializer for `Product` model
    """
    vendor = VendorSerializer(many=True)
    categories = CategoryProductSerializer(many=True)
    sale = SaleSerializer()
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)
    related_products = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'rating',
                  'cost', 'sale', 'final_cost', 'amount', 'slug',
                  'related_products', 'images', 'videos', 'tags',
                  'vendor', 'categories', 'specs',)
        read_only_fields = ('vendor', 'slug', 'final_cost', )

    def get_related_products(self, obj):
        qs = obj.related_products.all()
        return ProductRelatedProductSerializer(qs, many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    """
    Used for GET requests for `Product` model
    """
    vendor = VendorSerializer(many=True)
    categories = CategoryProductSerializer(many=True)
    sale = serializers.StringRelatedField(many=False)
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'rating',
                  'slug', 'images', 'videos',
                  'cost', 'sale', 'final_cost',
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
    related_products = ProductRelatedProductSerializer(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'cost', 'sale', 'final_cost',
                  'amount', 'slug', 'related_products', 'uploaded_images',
                  'uploaded_videos', 'tags', 'vendor', 'categories',
                  'specs', 'images', 'videos')
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
    categories = CategoryProductSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'cost', 'sale', 'final_cost',
                  'amount', 'slug', 'tags', 'vendor', 'categories', 'images')


class ProductUserRelationSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'images', 'cost', 'final_cost')

    def get_images(self, obj):
        return ImageSerializer(obj.images.all()[0]).data
