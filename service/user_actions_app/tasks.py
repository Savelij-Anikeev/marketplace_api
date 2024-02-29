from celery import shared_task
from product_app.ProductService import ProductService
from vendor_app.VendorService import VendorService
from product_app.models import Product


@shared_task()
def base_rating_counter(obj_id, is_pre_delete=False):
    # recalc for product
    product = Product.objects.get(pk=obj_id)
    product.rating = ProductService.get_rating(product)
    product.save()

    # get vendor and recalc rating for it
    for vendor in product.vendor.all():
        vendor.rating = VendorService.get_rating(vendor)
        vendor.save()
