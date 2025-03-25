from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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
from custom_permissions import IsAssignedToReportMeasure, IsSMAUser, ReportIsTheirs


class EnvironmentalPlanViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalPlan.objects.all()
    serializer_class = EnvironmentalPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  # I'm not sure if this is OK because the restriction above
        return [IsSMAUser()]  # Only SMA users can CRUD completely.

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


class MeasureReportViewSet(viewsets.ModelViewSet):
    queryset = MeasureReport.objects.all()
    serializer_class = MeasureReportSerializer
    authentication_classes = [JWTAuthentication]
    
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
   # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    
    
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
    authentication_classes = [JWTAuthentication]

    
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
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  
        return [IsSMAUser()]  # Only allow SMA users to write these
    
    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)
