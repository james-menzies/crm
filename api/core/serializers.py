from django.db.models import prefetch_related_objects
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from core.models import Client, Product, Membership, Order, OrderItem


class WriteableNestedField(serializers.PrimaryKeyRelatedField):

    def __init__(self, queryset, **kwargs):
        self.queryset = queryset
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, instance):
        return ItemStub(instance).data

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


    product = WriteableNestedField(queryset=Product.objects)
    subtotal = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        if 'type' in validated_data and instance.type != validated_data['type']:
            raise serializers.ValidationError({'type': 'Cannot alter type once created.'})

        return super().update(instance, validated_data)

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
        prefetch_related_objects([order], 'items', 'items__product')
        return order

    def _create_items(self, item_data):
        items = []
        existing_product_ids = set()



    total = serializers.IntegerField(read_only=True)
    client = WriteableNestedField(queryset=Client.objects)

class ItemStub(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
