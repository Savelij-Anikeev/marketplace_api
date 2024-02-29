from django.db import transaction
from django.db.models import F

from .models import Status
from product_app.models import Product 

from shopping_cart_app.CartService import CartService


class OrderService:
    
    @staticmethod
    def create_order(serializer, req):
        with transaction.atomic():
            # changing amount of product
            product_list = req.data.get('products')
            product_info = []

            # getting dict with product's id and amount
            for product in product_list:
                product_info.append({
                    "product_id": product.get('product').get('id'),
                    "product_amount": product.get('amount'),})
            
            # selecting products for update and updating
            product_qs = Product.objects.select_for_update().filter(pk__in=[i.get('product_id') for i in product_info])
            for prod in product_info:
                p_id, p_amount = prod.get('product_id'), prod.get('product_amount')
                inst = product_qs.filter(pk=p_id)[0]
                inst.amount -= p_amount
                inst.save()


            # creating order
            serializer.validated_data['user'] = req.user
            serializer.validated_data['cost'] = req.data.get('cost')
            serializer.validated_data['products'] = req.data.get('products')
            instance = serializer.save()
            instance.statuses.set = (Status.objects.create(order=instance, status=1).pk, )

            # clearing rels
            CartService.delete_items(user_id=req.user.pk)
            