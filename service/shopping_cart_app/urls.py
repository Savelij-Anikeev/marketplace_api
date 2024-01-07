from rest_framework import routers

from .views import CartProductRelationViewSet


router = routers.SimpleRouter()
router.register('cart', CartProductRelationViewSet)

urlpatterns = [

] + router.urls

"""
* if there is no cart for current user add one

cart/ - crud operations with *relations
cart/<index>/ - get product by index in queryset

* - CartProductRelationViewSet
"""
