from django.contrib import admin

from .models import AnalyticsReport


# Register your models here.

@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ("user", "report_type", "created_at", "file")
    search_fields = ("user__username", "report_type")
    list_filter = ("report_type", "created_at")