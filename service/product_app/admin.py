from django.contrib import admin

from .models import Product, Category, Vendor, Sale

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Sale)

