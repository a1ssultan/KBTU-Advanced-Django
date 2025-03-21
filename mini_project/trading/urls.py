from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trading.views import OrderViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
