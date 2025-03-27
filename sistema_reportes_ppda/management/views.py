from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from management.models import (
    EnvironmentalPlan,
    Measure,
    MeasureReport,
    ReportFile,
    Body,
    BodyMeasure,
)
from management.serializers import (
    EnvironmentalPlanSerializer,
    MeasureReportSerializer,
    MeasureSerializer,
    ReportFileSerializer,
    BodySerializer,
    BodyMeasureSerializer,
)
from custom_permissions import IsAssignedToReportMeasure, IsSMAUserOrAdmin, ReportIsTheirs


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

    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  # I'm not sure if this is OK because the restriction above
        return [IsSMAUserOrAdmin()]  # Only SMA users can CRUD completely.

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


class MeasureReportViewSet(viewsets.ModelViewSet):
    queryset = MeasureReport.objects.all()
    serializer_class = MeasureReportSerializer
    
    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  # Anyone can read (for now)
        return [IsAssignedToReportMeasure()]  # Only users from assigned bodies

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


class ReportFileViewSet(viewsets.ModelViewSet):
    queryset = ReportFile.objects.all()
    serializer_class = ReportFileSerializer
    
    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  # Anyone can read (for now)
        return [ReportIsTheirs()]  # Only if the related reports is assigned to the user's body  

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


class BodyViewSet(viewsets.ModelViewSet):
    queryset = Body.objects.all()
    serializer_class = BodySerializer
    
    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  
        return [IsAdminUser()]  # Because of fixed nature of the objects, only allow Admins to modify list

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


class BodyMeasureViewSet(viewsets.ModelViewSet):
    queryset = BodyMeasure.objects.all()
    serializer_class = BodyMeasureSerializer

    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  
        return [IsSMAUserOrAdmin()]  # Only allow SMA users to write these
    
    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)
