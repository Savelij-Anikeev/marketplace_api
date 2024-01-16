import uuid

from django.db.models import Sum, Prefetch
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
        vendors = ' '.join(list(map(str, serializer.validated_data['vendor'])))
        slug_data = serializer.validated_data['name'] + ' by ' + vendors + str(uuid.uuid4())[:25]
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
        from product_app.models import Product
        relations = CartProductRelation.objects.filter(product=product).prefetch_related(
                                                    Prefetch('product', Product.objects.all()))
        # find relations with Product
        for relation in relations:
            relation.product_cost = CartProductService.calc_product_cost(
                amount=relation.amount,
                final_cost=product.final_cost
            )
            relation.save()

    @staticmethod
    def get_rating(obj):
        from user_actions_app.models import Review
        from django.core import cache

        qs = Review.objects.filter(product_id=obj.pk).prefetch_related('author')
        qs_len = qs.count()
        grade_sum = qs.aggregate(Sum("grade")).get('grade__sum')
        if qs_len == 0: return 0

        return round(grade_sum / qs_len, 2)

    @staticmethod
    def check_static(validated_data):
        uploaded_images = uploaded_videos = None

        if validated_data.get("uploaded_images") is not None:
            uploaded_images = validated_data.pop("uploaded_images")
        if validated_data.get("uploaded_videos") is not None:
            uploaded_videos = validated_data.pop("uploaded_videos")

        return uploaded_images, uploaded_videos

    @staticmethod
    def give_static(uploaded_images, uploaded_videos, instance):
        from static_app.models import Image, Video

        if uploaded_images:
            for img in uploaded_images:
                Image.objects.create(content_object=instance, object_id=instance.pk, url=img)

        if uploaded_videos:
            for vid in uploaded_videos:
                Video.objects.create(content_object=instance, object_id=instance.pk, url=vid)