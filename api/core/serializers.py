from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField

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

    subtotal = serializers.IntegerField(read_only=True)

    def validate(self, data):

        if 'type' not in data:
            return data

        if data['type'] == 'membership' and 'membership' not in data:
            raise serializers.ValidationError({'membership': 'This field is required.'})

        if data['type'] == 'product' and 'product' not in data:
            raise serializers.ValidationError({'product': 'This field is required.'})

        return data


class OrderSerializer(serializers.ModelSerializer):
    """
    This class can optionally take the `include_items` flag on instantiation
    which will render the order items out to the user. Default false.
    """

    def __init__(self, *args, include_items=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not include_items:
            self.fields.pop('items')

    class Meta:
        model = Order
        exclude = []

    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.IntegerField(read_only=True)
