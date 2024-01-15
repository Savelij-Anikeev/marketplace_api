from rest_framework import viewsets

from .serializers import VendorSerializer
from .models import Vendor


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
