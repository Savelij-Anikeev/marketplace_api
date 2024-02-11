from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from product_app.serializers import ProductUserRelationSerializer
from vendor_app.serializers import VendorSerializer
from .models import UserProductRelation, UserPostRelation

from .UserService import UserService


# user
class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(required=False)
    work_place = VendorSerializer(required=False, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'phone', 'work_place',
                  'role', 'is_superuser', 'is_active')

    def get_role(self, obj):
        return obj.role


class UserCreateSerializer(serializers.ModelSerializer):
    # role = serializers.SerializerMethodField()
    # password = serializers.CharField(required=True)
    # username = serializers.StringRelatedField(required=False, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password', 'phone', 'work_place', 'role', 'is_superuser')

    def get_role(self, obj):
        return obj.role

    def create(self, validated_data):
        """
        by default Django sets is_active == True,
        we change this behaviour.
        Although, we generate username for user
        through method of  `UserService`
        """
        validated_data['password'] =  make_password(validated_data['password'])
        validated_data['username'] = UserService.generate_username(
            first_name=validated_data['first_name'].lower(),
            last_name=validated_data['last_name'].lower()
        )
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


# user product
class UserProductRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProductRelation
        fields = ('is_favorite', 'product')


class UserProductRelationListSerializer(serializers.ModelSerializer):
    product = ProductUserRelationSerializer()

    class Meta:
        model = UserProductRelation
        fields = ('is_favorite', 'product')


# user post
class UserPostRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = '__all__'
