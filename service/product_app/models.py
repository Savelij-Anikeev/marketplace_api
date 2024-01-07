from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from user_actions_app.models import BasePost
from vendor_app.models import Vendor
from static_app.models import Image, Video

from slugify import slugify


class Product(BasePost, models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)

    sale = models.ForeignKey('Sale', on_delete=models.PROTECT, blank=True, null=True)
    cost = models.DecimalField(max_digits=100, decimal_places=2)
    final_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    amount = models.PositiveIntegerField(default=0)
    specs = models.JSONField()
    tags = models.CharField(max_length=256, null=True, blank=True)

    vendor = models.ManyToManyField(Vendor)
    categories = models.ManyToManyField('Category')

    slug = models.SlugField(default=slugify(str(name)))

    photos = GenericRelation(Image, null=True, blank=True)
    videos = GenericRelation(Video, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(BasePost, models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


# sales
class Sale(models.Model):
    percentage = models.PositiveIntegerField()  # add validator 0-100%

    def __str__(self):
        return f'{self.percentage}%'
