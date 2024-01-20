from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from user_actions_app.models import BasePost
from vendor_app.models import Vendor
from static_app.models import Image, Video

from slugify import slugify

from mptt.models import MPTTModel, TreeForeignKey, TreeManager


class Product(BasePost, models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)

    sale = models.ForeignKey('Sale', on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    cost = models.DecimalField(max_digits=100, decimal_places=2)
    final_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    amount = models.PositiveIntegerField(default=0)
    specs = models.JSONField(null=True)
    tags = models.CharField(max_length=256, null=True, blank=True)

    vendor = models.ManyToManyField(Vendor)
    categories = models.ManyToManyField('Category')

    slug = models.SlugField(default=slugify(str(name)), unique=True, max_length=500)

    related_products = models.ManyToManyField('Product', null=True, blank=True)
    images = GenericRelation(Image)
    videos = GenericRelation(Video)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Category(BasePost, MPTTModel):
    objects = TreeManager()

    name = models.CharField(max_length=128)
    parent = TreeForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


# sales
class Sale(models.Model):
    percentage = models.PositiveIntegerField()  # add validator 0-100%
    expire_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        status = 'active' if self.is_active else 'expired'
        return f'{self.percentage}% - {status}'
