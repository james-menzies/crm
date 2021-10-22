from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from core.models import Client, Membership, Product
from core.serializers import ClientSerializer, MembershipSerializer, ProductSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
