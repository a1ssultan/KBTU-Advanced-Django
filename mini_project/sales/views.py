from decimal import Decimal

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from trading.models import Transaction
from users.permissions import IsAdmin, IsOwnerOrAdmin
from .models import SalesOrder, Promotion, Invoice
from .serializers import SalesOrderSerializer, PromotionSerializer, InvoiceSerializer


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SalesOrder.objects.all().select_related("customer", "product", "discount")
        return SalesOrder.objects.filter(customer=user).select_related("product", "discount")

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def apply_promo_code(self, request, pk=None):
        order = self.get_object()
        promo_code = request.data.get("promo_code")

        if not promo_code:
            return Response({"error": "Промокод не указан"}, status=status.HTTP_400_BAD_REQUEST)

        promo = Promotion.objects.filter(promo_code=promo_code).first()
        if not promo or not promo.is_active():
            return Response({"error": "Неверный или неактивный промокод"}, status=status.HTTP_400_BAD_REQUEST)

        order.discount = promo
        order.save()
        return Response({"message": "Промокод применен!", "final_price": order.final_price}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def complete(self, request, pk=None):
        order = self.get_object()
        order.mark_as_completed()
        return Response({"status": "completed"})

    @action(detail=True, methods=["post"], permission_classes=[IsOwnerOrAdmin])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.mark_as_canceled()
        return Response({"status": "canceled"})


class PromotionViewSet(viewsets.ModelViewSet):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Promotion.objects.all()


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Invoice.objects.all().select_related("sales_order__customer", "sales_order__product")
        return Invoice.objects.filter(sales_order__customer=user).select_related("sales_order__product")

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def download(self, request, pk=None):
        invoice = self.get_object()
        return invoice.get_pdf_response()
