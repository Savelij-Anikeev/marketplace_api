from django.db.models import Sum
from djoser.serializers import UserSerializer

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from product_app.models import Product
from product_app.serializers import ProductListSerializer, ProductCartSerializer
from .models import Cart, CartProductRelation


class CartProductRelationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProductRelation
        fields = ('id', 'cart', 'amount', 'product_cost', 'product')
        read_only_fields = ('cart', 'product_cost')


class CartProductRelationCartSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer()

    class Meta:
        model = CartProductRelation
        fields = ('amount', 'product_cost', 'product')


class CartProductRelationGeneralSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartProductRelation
        fields = ('id', 'cart', 'amount', 'product_cost', 'product')


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    products = CartProductRelationCartSerializer(many=True)
    cost = serializers.SerializerMethodField()
    is_valid = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cost', 'is_valid', 'detail', 'products')

    def get_cost(self, obj):
        cost = obj.products.all().aggregate(Sum('product_cost')).get('product_cost__sum')
        return cost

    def get_detail(self, obj):
        return self.check_items(obj)[1]

    def get_is_valid(self, obj):
        # get each relation and check if there is enough amount of product
        return self.check_items(obj)[0]

    def check_items(self, obj):
        details = []
        is_valid = True

        for relation in obj.products.all():
            current_amount = relation.amount
            product = Product.objects.get(pk=relation.product.id)
            if current_amount > product.amount:
                is_valid = False
                details.append(f'Max `{product}` amount is {product.amount}')

        return is_valid, details
