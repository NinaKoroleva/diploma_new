from rest_framework import serializers
from .models import Product, Order, OrderItem, Contact, ProductInfo


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category"
        ]

class ProductInfoSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductInfo
        fields = [
            "id",
            "product",
            "price",
            "price_rrc",
            "quantity",
            "shop"
        ]
class OrderItemSerializer(serializers.ModelSerializer):

    product = serializers.CharField(
        source="product_info.product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "quantity"
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "state",
            "dt",
            "items"
        ]


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            "id",
            "city",
            "street",
            "house",
            "phone"
        ]