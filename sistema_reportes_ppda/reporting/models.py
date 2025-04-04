from django.db import models

from management.models import EnvironmentalPlan


# Create your models here.
class ProgressReport(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    environmental_plan = models.ForeignKey(
        EnvironmentalPlan, on_delete=models.PROTECT, related_name="progress_reports"
    )
    publication_date = models.DateField()
    data_created = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="created_progress_reports",
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="updated_progress_reports",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.environmental_plan.short_name})"


class ProgressReportData(models.Model):
    progress_report = models.OneToOneField(
        ProgressReport, on_delete=models.CASCADE, related_name="data"
    )
    data = models.JSONField()  # Store data as JSON (first approach)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Data for report {self.progress_report.name} - {self.created_at}"
