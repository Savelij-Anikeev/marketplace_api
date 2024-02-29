from rest_framework import routers

from .views import ProductViewSet, CategoryViewSet, SaleViewSet

router = routers.SimpleRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('sales', SaleViewSet)

urlpatterns = [

]

urlpatterns += router.urls
