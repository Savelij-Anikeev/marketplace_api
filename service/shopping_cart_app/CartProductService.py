from django.http import Http404

from shopping_cart_app.models import Cart


class CartProductService:
    @staticmethod
    def get_queryset(request):
        obj, _ = Cart.objects.get_or_create(user=request.user)
        if obj.products.all():
            return obj.products.all()
        raise Http404

    @staticmethod
    def perform_create(serializer, request):
        current_cart = Cart.objects.get_or_create(user=request.user)[0]
        current_product = serializer.validated_data['product']
        current_relations = current_cart.products.all().prefetch_related('product')

        serializer.validated_data['cart'] = current_cart

        for rel in current_relations:
            if rel.product == current_product:
                rel.amount = serializer.validated_data['amount']
                rel.product_cost = CartProductService.calc_product_cost(rel.product.final_cost,
                                                                        rel.amount)
                rel.save()
                break
        else:
            rel = serializer.save()
            rel.product_cost = CartProductService.calc_product_cost(rel.product.final_cost,
                                                                    rel.amount)
            rel.save()

    @staticmethod
    def calc_product_cost(final_cost, amount):
        product_cost = float(final_cost) * amount
        return product_cost

    @staticmethod
    def get_object(qs, kwargs):
        pk = int(kwargs.get('pk'))
        if pk < 1: raise Http404

        try:
            return qs[pk - 1]
        except IndexError:
            raise Http404

