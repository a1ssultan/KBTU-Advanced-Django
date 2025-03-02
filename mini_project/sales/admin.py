from django.contrib import admin

from sales.models import Promotion, SalesOrder, Invoice


# Register your models here.

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("name", "discount_type", "discount_value", "promo_code", "start_date", "end_date", "is_active")
    search_fields = ("name", "promo_code")
    list_filter = ("discount_type", "start_date", "end_date")


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "quantity", "unit_price", "final_price", "status", "created_at")
    search_fields = ("customer__username", "product__name")
    list_filter = ("status", "created_at")
    readonly_fields = ("final_price",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("sales_order", "total_amount", "issued_at")
    search_fields = ("sales_order__customer__username", "sales_order__product__name")
    readonly_fields = ("total_amount", "issued_at")