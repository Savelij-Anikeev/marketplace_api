from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from product_app.models import Product


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class CartProductRelation(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    product_cost = models.PositiveIntegerField(null=True)
