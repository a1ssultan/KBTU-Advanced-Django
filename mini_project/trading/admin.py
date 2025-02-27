from django.contrib import admin
from .models import Order, Transaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "order_type", "quantity", "status", "created_at")
    list_filter = ("status", "order_type", "created_at")
    search_fields = ("user__username", "product__name")
    ordering = ("-created_at",)
    actions = ["mark_completed", "mark_canceled"]

    def mark_completed(self, request, queryset):
        queryset.update(status="completed")
    mark_completed.short_description = "Mark selected orders as Completed"

    def mark_canceled(self, request, queryset):
        queryset.update(status="canceled")
    mark_canceled.short_description = "Mark selected orders as Canceled"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "price", "executed_at")
    list_filter = ("executed_at",)
    search_fields = ("order__user__username", "order__product__name")
    ordering = ("-executed_at",)
