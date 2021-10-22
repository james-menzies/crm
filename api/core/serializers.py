from rest_framework import serializers

from core.models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        exclude = []

