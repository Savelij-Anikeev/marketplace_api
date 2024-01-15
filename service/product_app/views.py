from django.db.models import Prefetch, Q

from rest_framework import viewsets, permissions
from rest_framework.permissions import SAFE_METHODS

from django_filters.rest_framework import DjangoFilterBackend

from static_app.models import Video, Image
from vendor_app.models import Vendor
from .models import Product, Category, Sale
from .permissions import IsAdminOrVendorStaff
from .serializers import (ProductDetailSerializer, ProductListSerializer, ProductChangeSerializer,
                          ProductCreateSerializer, CategorySerializer, SaleSerializer)

from .ProductService import ProductService
from .filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product APIView
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    queryset = Product.objects.all().prefetch_related(Prefetch('vendor', Vendor.objects.all()),
                                                      Prefetch('images', Image.objects.all()),
                                                      Prefetch('videos', Video.objects.all()),)

    def get_serializer_class(self):
        """
        selecting serializer
        """
        match self.action:
            case 'retrieve': return ProductDetailSerializer
            case 'list': return ProductListSerializer
            case 'create': return ProductCreateSerializer
            case _: return ProductChangeSerializer

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
        if not serializer.validated_data.get('vendor'):
            serializer.validated_data['vendor'] = [self.request.user.work_place]

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
    queryset = Category.objects.all().prefetch_related('sub_category')
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (permissions.IsAdminUser, )
        else:
            self.permission_classes = ()

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if self.kwargs.get('only_top_categories'):
            return Category.objects.filter(~Q(sub_category=0)).prefetch_related('sub_category')
        return self.queryset


class SaleViewSet(viewsets.ModelViewSet):
    """
    Sale APIView
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


