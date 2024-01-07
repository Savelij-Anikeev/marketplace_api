from django.http.response import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from .serializers import CartSerializer, CartProductRelationCreateSerializer, CartProductRelationGeneralSerializer
from .models import Cart, CartProductRelation

from .CartProductService import CartProductService


class CartListDetailAPIView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            generics.GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartProductRelationViewSet(viewsets.ModelViewSet):
    queryset = CartProductRelation.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        getting products by user
        """
        qs = CartProductService.get_queryset(self.request)
        return qs

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return CartProductRelationCreateSerializer
        return CartProductRelationGeneralSerializer

    def perform_create(self, serializer):
        # put logic into CartService
        # get cart
        CartProductService.perform_create(serializer=serializer, request=self.request)

    def get_object(self):
        qs = self.get_queryset()
        return CartProductService.get_object(qs, self.kwargs)

    def perform_update(self, serializer):
        final_cost = serializer.validated_data['product'].final_cost
        amount = serializer.validated_data['amount']
        serializer.validated_data['product_cost'] = CartProductService.calc_product_cost(final_cost, amount)
        serializer.save()
