from rest_framework import viewsets
from reporting.models import ProgressReport
from reporting.serializers import ProgressReportSerializer
from custom_permissions import IsSMAUser


class ProgressReportViewSet(viewsets.ModelViewSet):
    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer
    permission_classes = [IsSMAUser]
    
    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)