class VendorService:
    @staticmethod
    def get_rating(obj):
        from product_app.models import Product

        qs = Product.objects.all()
        rating_sum = count = 0

        for instance in qs:
            if obj in instance.vendor.all() and instance.rating > 0:
                rating_sum += instance.rating
                count += 1

        if count == 0:
            return 0
        return round(rating_sum / count, 2)
