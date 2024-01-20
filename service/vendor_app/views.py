from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import VendorSerializer
from .models import Vendor


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (IsAdminUser,)
