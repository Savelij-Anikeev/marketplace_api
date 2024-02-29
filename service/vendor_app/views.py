from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdminOrManager

from .serializers import VendorSerializer, WorkerSerializer
from .models import Vendor


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes =  (IsAuthenticated, IsAdminOrManager)

        return [permission() for permission in self.permission_classes]

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.filter(~Q(role='default'))
    serializer_class = WorkerSerializer
    permission_classes = (IsAuthenticated, IsAdminOrManager)
    
    def post(self, *args, **kwargs):
        # getting user, role from request
        user_pk = self.request.data.get('user')
        role = self.request.data.get('role')
        vendors = Vendor.objects.filter(pk=self.kwargs.get('vendor_pk'))
        qs = get_user_model().objects.filter(pk=int(user_pk))

        if not vendors.exists(): 
            return Response({'detail': f'vendor with pk {self.kwargs.get("vendor_pk")} doesn\'t exist'})
        if not qs.exists(): 
            return Response({'detail': f'user with pk {user_pk} doesn\'t exist'})
        
        isnt = qs[0]
        isnt.role = role
        isnt.work_place = vendors[0]
        isnt.save()

        return Response({'result': self.serializer_class(isnt).data})

    def destroy(self, request, *args, **kwargs):
        inst = self.get_object()
        inst.role = 'default'
        inst.work_place = None
        inst.save()

        return Response({'detailt': 'success'})
