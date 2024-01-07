from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from product_app.models import Product
from product_app.serializers import ProductListSerializer
from .models import Cart, CartProductRelation


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartProductRelationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProductRelation
        fields = ('id', 'cart', 'amount', 'product_cost', 'product')
        read_only_fields = ('cart', 'product_cost')


class CartProductRelationGeneralSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartProductRelation
        fields = ('id', 'cart', 'amount', 'product_cost', 'product')

