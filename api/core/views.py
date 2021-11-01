# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from core.models import Client, Membership, Product, Order, OrderItem
from core.serializers import ClientSerializer, MembershipSerializer, ProductSerializer, \
    OrderSerializer, OrderItemSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items')
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ViewSet):

    def create(self, request, **kwargs):
        return Response({'hello': 'world'})


    def update(self, request, **kwargs):
        serializer = OrderItemSerializer(many=True, data=request.data)
        order = Order.objects.get(id=kwargs['id'])


        if serializer.is_valid():
            serializer.save(order=order)
            return Response("done")
        else:
            return Response("error")


    def get_queryset(self):
        order_id = self.kwargs['id']
        queryset = OrderItem.objects.filter(order=order_id)
        return queryset

    queryset = OrderItem.objects

    serializer_class = OrderItemSerializer
