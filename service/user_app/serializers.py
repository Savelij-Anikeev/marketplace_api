from django.contrib.auth import get_user_model
from rest_framework import serializers

from product_app.serializers import ProductListSerializer
from vendor_app.serializers import VendorSerializer
from .models import User, UserProductRelation, UserPostRelation


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    work_place = VendorSerializer()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'work_place', 'role', 'is_superuser')

    def get_role(self, obj):
        return obj.role


class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'work_place', 'role', 'is_superuser')

    def get_role(self, obj):
        return obj.role


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'work_place', 'role', 'is_superuser')

    def get_role(self, obj):
        return obj.role


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'photo', 'username')


class UserProductRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = '__all__'


class UserProductRelationListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    user = UserAnswerSerializer()

    class Meta:
        model = UserProductRelation
        fields = ('id', 'user', 'is_favorite', 'product')


class UserPostRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = '__all__'
