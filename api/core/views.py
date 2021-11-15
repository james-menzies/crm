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
    queryset = Order.objects.select_related('client').prefetch_related('items')
    serializer_class = OrderSerializer

    def get_object(self):

        order = get_object_or_404(self.queryset, **self.kwargs)

        if order.is_complete:
            raise PermissionDenied('No!', 400)

        return order

    def partial_update(self, request, *args, **kwargs):
        return self._update(request.data, partial=True)

    def update(self, request, *args, **kwargs):
        return self._update(request.data)

    def _update(self, data, partial=False):
        order = self.get_object()
        serializer = self.serializer_class(instance=order, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        if order.is_complete:
            membership_item : OrderItem = [item for item in order.items.all() if item.type == 'membership'][0]



        return Response(serializer.data)


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
