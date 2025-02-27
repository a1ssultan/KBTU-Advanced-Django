from decimal import Decimal

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from trading.models import Order, Transaction
from trading.serializers import OrderSerializer, TransactionSerializer
from users.permissions import IsAdmin, IsOwnerOrAdmin


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.with_related()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def complete(self, request, pk=None):
        order = self.get_object()
        order.mark_as_completed()
        Transaction.objects.create(order=order, price=Decimal(order.product.price) * order.quantity)
        return Response({"status": "completed"})

    @action(detail=True, methods=["post"], permission_classes=[IsOwnerOrAdmin])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.mark_as_canceled()
        return Response({"status": "canceled"})


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.with_related()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.has_perm("trading.view_all_transactions"):
            return Transaction.objects.with_related()
        return Transaction.objects.filter(order__user=user)
