from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from core.models import Client
from core.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

