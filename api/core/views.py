# Create your views here.
from datetime import date
from typing import List

from dateutil.relativedelta import relativedelta
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
    serializer_class = OrderSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return self.serializer_class(*args, include_items=False, **kwargs)

        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        queryset = Order.objects.select_related('client').prefetch_related('items')

        if self.detail:
            queryset = queryset.prefetch_related('items__product')

        return queryset

    def get_object(self):

        order = get_object_or_404(self.get_queryset(), **self.kwargs)

        if order.is_complete:
            raise PermissionDenied('Cannot alter completed order.', 400)

        return order

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        if order.is_complete:
            self._finalize_order(order)

        return Response({'order': order.id})

    def partial_update(self, request, *args, **kwargs):
        return self._update(request.data, partial=True)

    def update(self, request, *args, **kwargs):
        return self._update(request.data)

    def _update(self, data, partial=False):
        order = self.get_object()
        serializer = self.serializer_class(instance=order, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        if order.is_complete:
            self._finalize_order(order)

        return Response({'status': 'Success'})

    def _finalize_order(self, order: Order):
        memberships: List[Membership] = Membership.objects.filter(
            orderitem__order=order.id).all()

        if len(memberships) == 0:
            return

        end_date = max([date.today(), order.client.membership_expiry])
        years_added = 0
        months_added = 0

        for membership in memberships:
            if membership.period_type == 'y':
                years_added += membership.period_amount
            else:
                months_added += membership.period_amount

        end_date += relativedelta(months=+months_added, years=+years_added)
        Client.objects.filter(pk=order.client_id).update(membership_expiry=end_date)


class OrderItemViewSet(viewsets.GenericViewSet,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order_id = self.kwargs['id']
        queryset = OrderItem.objects.filter(order=order_id)
        return queryset

    def check_order(self):
        order = get_object_or_404(Order.objects.all().only('is_complete'), pk=self.kwargs['id'])

        if order.is_complete:
            raise PermissionDenied('Cannot alter complete order', 400)

    def get_object(self):

        self.check_order()
        return super().get_object()

    def destroy_all(self, request, **kwargs):
        self.check_order()
        self.get_queryset().delete()
        return Response({'status': 'Success'})

    def create(self, request, **kwargs):
        self.check_order()
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(order_id=kwargs['id'])
        return Response(serializer.data)
