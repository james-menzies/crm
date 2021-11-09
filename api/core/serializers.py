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

    subtotal = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(write_only=True, required=False)
    membership_id = serializers.IntegerField(write_only=True, required=False)

    def create(self, validated_data):

        if validated_data['type'] == 'membership':
            membership_id = validated_data.pop('membership_id')

            try:
                membership = Membership.objects.get(pk=membership_id)
                order_item = OrderItem(**validated_data)
                order_item.membership = membership
                order_item.save()
            except Membership.DoesNotExist:
                raise serializers.ValidationError({'membership_id': 'Invalid membership id.'})
        else:
            product_id = validated_data.pop('product_id')
            try:
                product = Product.objects.get(pk=product_id)
                order_item = OrderItem(**validated_data)
                order_item.product = product
                order_item.save()
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_id': 'Invalid product id.'})



    def validate(self, data):

        if 'type' not in data:
            return data

        if data['type'] == 'membership' and 'membership_id' not in data:
            raise serializers.ValidationError({'membership_id': 'This field is required.'})

        if data['type'] == 'product' and 'product_id' not in data:
            raise serializers.ValidationError({'product_id': 'This field is required.'})


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


