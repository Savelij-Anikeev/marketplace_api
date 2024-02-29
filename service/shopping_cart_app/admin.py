from django.contrib import admin

from .models import Cart, CartProductRelation

admin.site.register(Cart)
admin.site.register(CartProductRelation)
