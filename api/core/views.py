# Create your views here.
from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
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

    def check_status(self, lookup: int):

        order = Order.objects.get(pk=lookup)
        if order.is_complete:
            raise PermissionDenied('No!', 400)

    def update(self, request, *args, **kwargs):
        self.check_status(kwargs['pk'])
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.check_status(kwargs['pk'])
        return super().partial_update(request, *args, **kwargs)

    def complete_order(self, order):
        """Check if order is set to be finalized. If so, update the membership
        status of the Client"""
        if not order.is_complete:
            return

        memberships = [item for item in order.items.all() if item.type == 'membership']





class OrderItemViewSet(viewsets.GenericViewSet,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin):
    serializer_class = OrderItemSerializer

    def update_all(self, request, **kwargs):
        return self.handle_create(request, update=True, **kwargs)

    def destroy_all(self, request, **kwargs):
        self.get_queryset().delete()
        return Response({'status': 'Success'})

    def create(self, request, **kwargs):
        return self.handle_create(request, **kwargs)

    def handle_create(self, request, update=False, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        order = get_object_or_404(Order.objects.all(), pk=kwargs['id'])

        if order.is_complete:
            raise PermissionDenied('Cannot alter complete order', 400)

        serializer.is_valid(raise_exception=True)

        if update:
            self.get_queryset().delete()

        serializer.save(order=order)
        return Response(OrderSerializer(order).data)

    def get_queryset(self):
        order_id = self.kwargs['id']
        queryset = OrderItem.objects.filter(order=order_id)
        return queryset
