from django.urls import path
from rest_framework import routers

from .views import CartProductRelationViewSet, CartListDetailAPIView, CartProductRelationClearAPIView


router = routers.SimpleRouter()
router.register('cart/products', CartProductRelationViewSet)

urlpatterns = [
    path('cart/', CartListDetailAPIView.as_view()),
    path('cart/clear/', CartProductRelationClearAPIView.as_view(), name='cart_clear'),
    # path('cart/do_order/', DoOrder.as_view()),
] + router.urls
