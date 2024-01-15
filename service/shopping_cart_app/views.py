import os
import requests
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from rest_framework import generics, viewsets, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.reverse import reverse

from product_app.models import Product
from .serializers import (CartSerializer, CartProductRelationCreateSerializer,
                          CartProductRelationGeneralSerializer, CartProductRelationCartSerializer)
from .models import Cart, CartProductRelation

from .CartProductService import CartProductService


class CartListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all().prefetch_related(
        Prefetch('products', CartProductRelation.objects.all()),
    )
    serializer_class = CartSerializer

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)


class CartProductRelationViewSet(viewsets.ModelViewSet):
    queryset = CartProductRelation.objects.all().prefetch_related(
        Prefetch('cart', Cart.objects.all()),
        Prefetch('product', Product.objects.all()),)
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


class CartProductRelationClearAPIView(generics.DestroyAPIView):
    queryset = CartProductRelation.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.get_queryset().filter(cart=Cart.objects.get(user=self.request.user))

    def destroy(self, request, *args, **kwargs):
        qs = self.get_object()
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class DoOrder(views.APIView):
#     permission_classes = (IsAuthenticated, )
#
#     def post(self, *args, **kwargs):
#         # creating new order
#         order_service = (os.getenv('ORDER_SERVICE_PROTOCOL') + '://' + os.getenv('ORDER_SERVICE_URL')
#                          + ':' + os.getenv('ORDER_SERVICE_PORT') + '/api/v1/orders/')
#         cart = Cart.objects.get(user=self.request.user)
#         request_data = CartSerializer(cart).data
#
#         if request_data['products'] is None:
#             return Response({'detail': 'You have to add products to cart before creating order!'})
#
#         requests.request(method='POST', url=order_service, data=request_data)
#
#         # clearing cart
#         HttpResponseRedirect(redirect_to=reverse('cart_clear'))
#
#     def get(self, request):
#         return Response({'status': 'You should do empty \POST\ request \n to make new order'})
