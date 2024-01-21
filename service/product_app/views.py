from django.db.models import Prefetch
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from rest_framework import viewsets, permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from static_app.models import Video, Image
from vendor_app.models import Vendor
from .models import Product, Category, Sale

from .ProductService import ProductService
from .filters import ProductFilter
from .permissions import IsAdminOrVendorStaff
from .serializers import (ProductDetailSerializer, ProductListSerializer, ProductChangeSerializer,
                          ProductCreateSerializer, CategorySerializer, SaleSerializer)


#ViewSets
class ProductViewSet(viewsets.ModelViewSet):
    """
    Product APIView
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    queryset = Product.objects.all().prefetch_related(Prefetch('vendor', Vendor.objects.all()),
                                                      Prefetch('images', Image.objects.all()),
                                                      Prefetch('videos', Video.objects.all()),
                                                      Prefetch('related_products', Product.objects.all()),)

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

    def create(self, request, *args, **kwargs):
        """
        Used to send custom response
        """
        from rest_framework.generics import get_object_or_404

        # checking if there is `sale` instance
        try:
            sale_instance = get_object_or_404(Sale, pk=int(request.data.get('sale')))
        except ValueError:
            sale_instance = None

        # checking `vendor` and putting user's `work_place` id
        # if it is empty
        try:
            if not request.data.get('vendor'):
                request.data['vendor'] = [request.user.work_place.pk]
        except AttributeError:
            return Response({'detail': '`vendor` field is empty! Check if user has `work_place` '
                                       'fields or send it in request body'})

        if sale_instance is not None:
            if not sale_instance.is_active:
                return Response({'detail': '`sale` in invalid, it is expired!'})

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Adding required information
        to the serializer and saving model
        """

        if not serializer.validated_data.get('vendor'):
            serializer.validated_data['vendor'] = [self.request.user.work_place]

        serializer.validated_data['slug'] = ProductService.get_slug(serializer=serializer)
        initial_cats = serializer.validated_data['categories']

        for category in initial_cats:
            ancestors = category.get_ancestors()
            if ancestors.exists():
                serializer.validated_data['categories'] += (*[i for i in ancestors], )

        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category APIView
    """
    queryset = Category.objects.all().prefetch_related('parent')
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (permissions.IsAdminUser, )
        else:
            self.permission_classes = ()

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        qs = [instance for instance in self.queryset if instance.parent is None]
        return qs


class SaleViewSet(viewsets.ModelViewSet):
    """
    Sale APIView
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (IsAdminOrVendorStaff,)


# Receivers
@receiver(post_save, sender=Product)
def manage_products_attrs_on_update(sender, instance, *args, **kwargs):
    if instance.sale is not None:
        ProductService.calc_final_price(instance)
    else:
        instance.final_cost = instance.cost


@receiver(pre_save, sender=Product)
def manage_products_attrs_on_update(sender, instance, *args, **kwargs):
    if instance.sale is not None:
        ProductService.calc_final_price(instance)
    else:
        instance.final_cost = instance.cost


@receiver(post_delete, sender=Sale)
def handle_deleted_sale_and_recalc_cost(sender, using, *args, **kwargs):
    from .tasks import change_final_cost
    change_final_cost.delay()

