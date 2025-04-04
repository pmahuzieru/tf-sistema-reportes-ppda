from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from reporting.models import ProgressReport
from reporting.serializers import ProgressReportSerializer
from custom_permissions import IsSMAUserOrAdmin
from management.models import EnvironmentalPlan


class ProgressReportViewSet(viewsets.ModelViewSet):
    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer

    def get_permissions(self):
        """
        Only SMA/Admin can create/update progress reports.
        Default permissions applied to other actions.
        """
        if self.action in ["create", "update", "partial_update"]:
            return [IsSMAUserOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)
