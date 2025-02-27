from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AnalyticsReport(models.Model):
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('trading', 'Trading Report'),
        ('revenue', 'Revenue Report'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"{self.report_type} - {self.created_at}"
