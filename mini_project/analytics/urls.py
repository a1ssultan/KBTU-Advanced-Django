from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsReportViewSet

router = DefaultRouter()
router.register(r"reports", AnalyticsReportViewSet, basename="analytics-report")

urlpatterns = [
    path("", include(router.urls)),
]
