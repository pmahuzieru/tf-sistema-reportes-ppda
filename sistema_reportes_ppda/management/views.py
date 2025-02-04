from rest_framework import viewsets
from management.models import EnvironmentalPlan, Measure, MeasureReport, ReportFile
from management.serializers import EnvironmentalPlanSerializer, MeasureReportSerializer, MeasureSerializer, ReportFileSerializer


class EnvironmentalPlanViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalPlan.objects.all()
    serializer_class = EnvironmentalPlanSerializer
    
    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)
        

class MeasureReportViewSet(viewsets.ModelViewSet):
    queryset = MeasureReport.objects.all()
    serializer_class = MeasureReportSerializer
    
    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)
        

class ReportFileViewSet(viewsets.ModelViewSet):
    queryset = ReportFile.objects.all()
    serializer_class = ReportFileSerializer
    
    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)