from slugify import slugify


class ProductService:
    """
    Initializes methods that contain
    business logic of `Product` model
    """
    @staticmethod
    def get_slug(serializer):
        """
        Getting slug from product name and vendor
        """
        slug_data = serializer.validated_data['name'] + ' by ' + str(serializer.validated_data['vendor'])
        return slugify(slug_data)

    @staticmethod
    def calculate_final_price(serializer):
        sale_amount = 1 - (serializer.validated_data['sale'].percentage / 100)
        result = sale_amount * float(serializer.validated_data['cost'])
        return result

    @staticmethod
    def recalculate_cost_relations(product):
        from shopping_cart_app.models import CartProductRelation
        from shopping_cart_app.CartProductService import CartProductService

        # get all related CartProductRelations
        relations = CartProductRelation.objects.filter(product=product)
        # find relations with Product
        for relation in relations:
            relation.product_cost = CartProductService.calc_product_cost(
                amount=relation.amount,
                final_cost=product.final_cost
            )
            relation.save()
