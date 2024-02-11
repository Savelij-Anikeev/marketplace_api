from .models import Cart


class CartService():
    @staticmethod
    def delete_items(user_id):
        inst = Cart.objects.filter(user_id=user_id)
        for rel in inst[0].products.all():
            rel.delete()