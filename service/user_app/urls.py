from django.urls import path

from rest_framework import routers

from .views import UserProductRelationAPIView, UserProductRelationList, UserPostRelationAPIView, UserViewSet


router = routers.SimpleRouter()
router.register('auth/users', UserViewSet)

urlpatterns = [
    path('products/<int:product_pk>/relation/', UserProductRelationAPIView.as_view()),
    path('auth/users/me/favorites/', UserProductRelationList.as_view()),
    # relations
    # path('products/<int:product_pk>/reviews/<int:review_pk>/relation/',
    #      UserPostRelationAPIView.as_view()),
    # path('products/<int:product_pk>/questions/<int:question_pk>/relation/',
    #      UserPostRelationAPIView.as_view()),
    # path('products/<int:product_pk>/reviews/<int:review_pk>/answer/<int:answer_pk>/relation/',
    #      UserPostRelationAPIView.as_view()),
    # path('products/<int:product_pk>/questions/<int:question_pk>/answer/<int:answer_pk>/relation/',
    #      UserPostRelationAPIView.as_view()),

] + router.urls
