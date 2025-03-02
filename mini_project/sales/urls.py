from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, PromotionViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r'orders', SalesOrderViewSet, basename='salesorder')
router.register(r'promotions', PromotionViewSet, basename='promotion')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]
