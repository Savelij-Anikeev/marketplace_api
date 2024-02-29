from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderSerializer

from .models import Order, Status

from .OrderService import OrderService
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderFilter


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter

    def create(self, request, *args, **kwargs):
        # accepting request with `Basket` serialized
        if not request.data.get('is_valid'):
            return Response({'detail': request.data.get('detail')})

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        OrderService.create_order(req=self.request, serializer=serializer)
    