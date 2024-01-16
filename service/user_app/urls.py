from django.urls import path

from rest_framework import routers

from .views import UserViewSet, UserProductRelationViewSet


router = routers.SimpleRouter()
router.register('auth/users', UserViewSet)
router.register('auth/users/me/favorites', UserProductRelationViewSet)

urlpatterns = router.urls
