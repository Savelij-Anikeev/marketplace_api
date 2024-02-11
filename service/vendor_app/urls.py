from django.urls import path

from rest_framework import routers

from .views import VendorViewSet, WorkerViewSet

router = routers.SimpleRouter()
router.register('vendors', VendorViewSet)

urlpatterns = [
    path('vendors/<int:vendor_pk>/workers/', WorkerViewSet.as_view({'get': 'list'})),
    path('vendors/<int:vendor_pk>/workers/<int:pk>/', WorkerViewSet.as_view({
        'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'})),
] + router.urls
