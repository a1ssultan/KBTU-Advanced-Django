from rest_framework import viewsets, permissions
from .models import AnalyticsReport
from .serializers import AnalyticsReportSerializer


class AnalyticsReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnalyticsReport.objects.all()
    serializer_class = AnalyticsReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AnalyticsReport.objects.all()
        return AnalyticsReport.objects.filter(user=user)
