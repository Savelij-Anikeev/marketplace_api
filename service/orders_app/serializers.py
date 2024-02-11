from rest_framework import serializers

from .models import Order, Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    statuses = StatusSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'user', 'cost', 'is_paid', 'products', 'statuses')
        read_only_fields = ('statuses', )
    
    # def get_cost(self, obj):
    #     c = 0
    #     for i in obj.products:
    #         c += i.get('product_cost')
    #     return c
