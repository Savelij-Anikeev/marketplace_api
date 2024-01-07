from rest_framework import viewsets, permissions
from rest_framework.permissions import SAFE_METHODS

from .models import Product, Category, Sale
from .permissions import IsAdminOrVendorStaff
from .serializers import (ProductDetailSerializer, ProductListSerializer, ProductChangeSerializer,
                          ProductCreateSerializer, CategorySerializer, SaleSerializer)

from .ProductService import ProductService


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product APIView
    """
    queryset = Product.objects.all()

    def get_serializer_class(self):
        """
        selecting serializer
        """
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action == 'list':
            return ProductListSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        return ProductChangeSerializer

    def get_permissions(self):
        """
        Only admin or vendor can do CRUD with instances
        """
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAdminOrVendorStaff, )
        else:
            self.permission_classes = ()

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        Adding required information
        to the serializer and saving model
        """
        serializer.validated_data['vendor'] = (self.request.user.work_place, )
        serializer.validated_data['slug'] = ProductService.get_slug(serializer=serializer)
        serializer.validated_data['final_cost'] = ProductService.calculate_final_price(serializer=serializer)

        serializer.save()

    def perform_update(self, serializer):
        """
        Calculating final cost and
        recalculating relations cost
        """
        serializer.validated_data['final_cost'] = ProductService.calculate_final_price(serializer)

        instance = serializer.save()
        ProductService.recalculate_cost_relations(instance)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category APIView
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (permissions.IsAdminUser, )
        else:
            self.permission_classes = ()

        return [permission() for permission in self.permission_classes]


class SaleViewSet(viewsets.ModelViewSet):
    """
    Sale APIView
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
