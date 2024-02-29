class SaleService:
    @staticmethod
    def handle_delete(instance):
        from product_app.models import Product

        for product in Product.objects.filter(sale=instance):
            product.final_cost = product.cost
            product.save()
