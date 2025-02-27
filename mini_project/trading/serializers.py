from rest_framework import serializers
from trading.models import Order, Transaction


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    order_type_display = serializers.CharField(source="get_order_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "product", "order_type", "order_type_display", "quantity", "status", "status_display", "created_at"]
        read_only_fields = ["status", "created_at"]


class TransactionSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "order", "price", "executed_at"]
        read_only_fields = ["executed_at"]
