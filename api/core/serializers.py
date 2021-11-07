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

    subtotal = serializers.IntegerField()
    product_id = serializers.IntegerField(write_only=True, required=False)
    membership_id = serializers.IntegerField(write_only=True, required=False)

    def validate(self, data):

        if 'type' not in data:
            return data

        if data['type'] == 'membership' and 'membership_id' not in data:
            raise serializers.ValidationError("membership_id must be provided.")

        if data['type'] == 'product' and 'product_id' not in data:
            raise serializers.ValidationError("product_id must be provided")

        return data

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = []

    items = OrderItemSerializer(many=True, read_only=True)

