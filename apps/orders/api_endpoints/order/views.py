from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from .serializers import (OrderSerializer, OrderListSerializer,
                          OrderUpdateWaiterSerializer, OrderUpdateClientSerializer)
from apps.orders.models import Order
from apps.users.models import UserRoles
from apps.common.permissions import IsClient, IsWaiter, IsAdmin


class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all().prefetch_related("items")
    serializer_class = OrderSerializer
    permission_classes = (IsClient,)
    parser_classes = (JSONParser,)
    filterset_fields = ('state', 'cancelled', 'payment_type',
                        'created_at', 'updated_at',)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderListSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.role == UserRoles.CLIENT:
            return self.queryset.filter(client=self.request.user)
        elif self.request.user.role == UserRoles.WAITER:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset

    def get_permissions(self):
        if self.request.method == "POST":
            return (IsClient(),)
        return (IsAuthenticated(),)


class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().prefetch_related("items")
    serializer_class = OrderSerializer
    permission_classes = (IsClient | IsWaiter,)
    parser_classes = (JSONParser,)
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsAuthenticated(),)
        elif self.request.method == 'DELETE':
            return (IsAdmin(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        if self.request.method in ['PUT', 'PATCH'] and self.request.user.role == UserRoles.CLIENT:
            return OrderUpdateClientSerializer
        if self.request.method in ['PUT', 'PATCH'] and self.request.user.role == UserRoles.WAITER:
            return OrderUpdateWaiterSerializer

    def get_queryset(self):
        if self.request.user.role == UserRoles.CLIENT:
            return self.queryset.filter(client=self.request.user)
        elif self.request.user.role == UserRoles.WAITER:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset
