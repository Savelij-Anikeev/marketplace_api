from rest_framework import routers

from .views import VendorViewSet

router = routers.SimpleRouter()
router.register('vendors', VendorViewSet)

urlpatterns = router.urls
