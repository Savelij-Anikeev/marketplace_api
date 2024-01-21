from django.contrib.auth import get_user_model
from rest_framework import serializers

from product_app.serializers import ProductListSerializer
from vendor_app.serializers import VendorSerializer
from .models import UserProductRelation, UserPostRelation


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(required=False)
    work_place = VendorSerializer(required=False, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'work_place', 'role', 'is_superuser', 'is_active')

    def get_role(self, obj):
        return obj.role


class UserCreateSerializer(serializers.ModelSerializer):
    # role = serializers.SerializerMethodField()
    # password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        #, 'work_place', 'role', 'is_superuser'

    def get_role(self, obj):
        return obj.role

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.is_active = False
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    work_place = serializers.IntegerField(required=False)
    role = serializers.CharField(required=False)

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
