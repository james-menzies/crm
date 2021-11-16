from rest_framework import serializers


class ItemStub(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class WriteableNestedField(serializers.PrimaryKeyRelatedField):

    def __init__(self, queryset, **kwargs):
        self.queryset = queryset
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, instance):
        return ItemStub(instance).data
