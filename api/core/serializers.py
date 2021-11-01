from rest_framework import serializers

from core.models import Client, Product, Membership, Order, OrderItem


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = []


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = []


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        exclude = []



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = []

    items = OrderItemSerializer(many=True, read_only=True)
