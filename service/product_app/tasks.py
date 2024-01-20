from django.apps import apps
from django.db.models import F
from django.utils import timezone

from celery import shared_task

from product_app.models import Product


@shared_task
def delete_expired_objects(model_name='Sale', app_name='product_app', **kwargs):
    # add command to `up` in make file to run
    # this task every time this app starts

    model = apps.get_model(app_name, model_name)
    for instance in model.objects.filter(expire_date__lt=timezone.now()):
        instance.is_active = False
        instance.save()
        related_products = instance.products.all()

        for product in related_products:
            # get each product delete sale and recalculate final_cost
            # save each instance
            product.sale = None
            product.final_cost = product.cost
            product.save()


@shared_task
def change_final_cost():
    Product.objects.filter(sale=None).update(final_cost=F('cost'))
