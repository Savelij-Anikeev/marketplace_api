from django.urls import path

from rest_framework import routers

from .views import UserProductRelationViewSet, UserPostRelationAPIView


router = routers.SimpleRouter()
router.register('auth/users/me/favorites', UserProductRelationViewSet)

urlpatterns = [
    # Review and Question urls
    path('products/<int:product_pk>/reviews/<int:review_pk>/relation/', UserPostRelationAPIView.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'})),
    path('products/<int:product_pk>/questions/<int:question_pk>/relation/', UserPostRelationAPIView.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'})),

    # Answer urls
    path('products/<int:product_pk>/reviews/<int:review_pk>/answers/<int:answer_pk>/relation/',
         UserPostRelationAPIView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    path('products/<int:product_pk>/questions/<int:question_pk>/answers/<int:answer_pk>/relation/',
         UserPostRelationAPIView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
] + router.urls
