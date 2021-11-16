from django.db.models import prefetch_related_objects
from rest_framework import serializers

from core.models import Client, Product, Membership, Order, OrderItem
from crm.serializers import WriteableNestedField


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    This class can optionally take the `include_items` flag on instantiation
    which will render the order items out to the user. Default True.
    """

    def __init__(self, *args, include_items=True, **kwargs):
        super().__init__(*args, **kwargs)
        if include_items:
            self.fields['items'] = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        item_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        items = [OrderItem(order=order, **data) for data in item_data]
        OrderItem.objects.bulk_create(items)
        return order

    total = serializers.IntegerField(read_only=True)
    client = WriteableNestedField(queryset=Client.objects)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']

    product = WriteableNestedField(queryset=Product.objects.all(), required=False)
    subtotal = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        """
        In order to help maintain the 'one-membership-per-order' rule,
        changing an order items type attribute is prohibited.
        """
        if 'type' in validated_data and instance.type != validated_data['type']:
            raise serializers.ValidationError({'type': 'Cannot alter type once created.'})

        return super().update(instance, validated_data)

    def validate(self, data):
        """
        It is really important here that the type attribute is respected.
        Validation will take place to ensure that the correct field is populated
        based on the type specified. If both are provided, the other field will
        be discarded.
        """
        if 'type' not in data:
            return data

        if data['type'] == 'membership' and 'membership' not in data:
            raise serializers.ValidationError({'membership': 'This field is required.'})

        if data['type'] == 'product' and 'product' not in data:
            raise serializers.ValidationError({'product': 'This field is required.'})

        if data['type'] == 'product':
            data.pop('membership', None)
        else:
            data.pop('product', None)

        return data
