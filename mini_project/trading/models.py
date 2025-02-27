from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product
from users.models import User


# Create your models here.


class OrderType(models.TextChoices):
    BUY = "buy", "Buy"
    SELL = "sell", "Sell"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    CANCELED = "canceled", "Canceled"


class OrderQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related("user", "product")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    order_type = models.CharField(max_length=15, choices=OrderType.choices)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=15, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = OrderQuerySet.as_manager()

    def __str__(self):
        return f"{self.user} - {self.get_order_type_display()} {self.quantity} {self.product}"

    class Meta:
        ordering = ["-created_at"]

    def mark_as_completed(self):
        self.status = OrderStatus.COMPLETED
        self.save(update_fields=["status"])

    def mark_as_canceled(self):
        self.status = OrderStatus.CANCELED
        self.save(update_fields=["status"])


class TransactionQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related("order", "order__user", "order__product")


class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transactions")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    executed_at = models.DateTimeField(auto_now_add=True)

    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return f"Transaction for Order #{self.order.id} at {self.price}"

    class Meta:
        ordering = ["-executed_at"]
