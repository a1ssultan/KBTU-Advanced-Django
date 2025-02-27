from rest_framework import serializers
from .models import SalesOrder, Invoice, Promotion


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["id", "name", "discount_type", "discount_value", "promo_code", "applicable_products", "start_date", "end_date"]
        read_only_fields = ["id"]


class SalesOrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount = PromotionSerializer(read_only=True)

    class Meta:
        model = SalesOrder
        fields = ["id", "customer", "product", "quantity", "unit_price", "status", "created_at", "total_price", "final_price", "discount"]
        read_only_fields = ["status", "created_at", "total_price", "unit_price", "final_price", "discount"]

    def get_total_price(self, obj):
        return obj.unit_price * obj.quantity


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["id", "sales_order", "total_amount", "issued_at"]
        read_only_fields = ["total_amount", "issued_at"]
