from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from products.models import Product
from users.models import User


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    discount_type = models.CharField(
        max_length=10,
        choices=[("fixed", "Fixed Amount"), ("percent", "Percentage")],
        default="percent"
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    promo_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    applicable_products = models.ManyToManyField(Product, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        from django.utils.timezone import now
        return self.start_date <= now() <= self.end_date

    def apply_discount(self, price):
        if self.discount_type == "fixed":
            return max(Decimal("0.01"), price - self.discount_value)
        elif self.discount_type == "percent":
            return max(Decimal("0.01"), price * (1 - self.discount_value / 100))
        return price

    def __str__(self):
        return f"{self.name} - {self.discount_value} ({self.discount_type})"


class SalesOrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    CANCELED = "canceled", "Canceled"


class SalesOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales_orders")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    discount = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=15, choices=SalesOrderStatus.choices, default=SalesOrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        base_price = self.product.price * self.quantity
        if self.discount and self.discount.is_active():
            self.final_price = self.discount.apply_discount(base_price)
        else:
            self.final_price = base_price
        super().save(*args, **kwargs)

    def mark_as_completed(self):
        self.status = SalesOrderStatus.COMPLETED
        self.save(update_fields=["status"])
        self.generate_invoice()

    def mark_as_canceled(self):
        self.status = SalesOrderStatus.CANCELED
        self.save(update_fields=["status"])

    def generate_invoice(self):
        invoice = Invoice.objects.create(sales_order=self, total_amount=self.final_price)
        invoice.generate_pdf()
        return invoice

    def __str__(self):
        return f"{self.customer} - {self.quantity} x {self.product} ({self.status})"


class Invoice(models.Model):
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name="invoice")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)

    def generate_pdf(self):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setTitle(f"Invoice_{self.id}")

        pdf.drawString(100, 800, f"Invoice ID: {self.id}")
        pdf.drawString(100, 780, f"Customer: {self.sales_order.customer.username}")
        pdf.drawString(100, 760, f"Product: {self.sales_order.product.name}")
        pdf.drawString(100, 740, f"Quantity: {self.sales_order.quantity}")
        pdf.drawString(100, 720, f"Unit Price: {self.sales_order.unit_price}")
        pdf.drawString(100, 700, f"Discount: {self.sales_order.discount.discount_value if self.sales_order.discount else 0}")
        pdf.drawString(100, 680, f"Total Amount: {self.total_amount}")
        pdf.drawString(100, 660, f"Issued At: {self.issued_at}")

        pdf.showPage()
        pdf.save()

        file_path = f"media/invoices/invoice_{self.id}.pdf"
        with open(file_path, "wb") as f:
            f.write(buffer.getvalue())

        return file_path

    def get_pdf_response(self):
        pdf_path = f"media/invoices/invoice_{self.id}.pdf"
        return FileResponse(open(pdf_path, "rb"), as_attachment=True, filename=f"Invoice_{self.id}.pdf")

    def __str__(self):
        return f"Invoice for {self.sales_order} - {self.total_amount}"
