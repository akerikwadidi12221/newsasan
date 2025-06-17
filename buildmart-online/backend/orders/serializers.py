from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'supplier',
            'quantity',
            'price_at_purchase',
            'created_at',
        ]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'user',
            'status',
            'total_amount',
            'shipping_address',
            'shipping_city',
            'shipping_postal_code',
            'payment_status',
            'created_at',
            'updated_at',
            'items',
        ]
