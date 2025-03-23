from rest_framework import serializers
from reporting.models import ProgressReport, ProgressReportData


class ProgressReportSerializer(serializers.ModelSerializer):
    environmental_plan = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="environmentalplan-detail"
    )

    class Meta:
        model = ProgressReport
        fields = "__all__"
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]

    def create(self, validated_data):
        """
        Will trigger Progress Report Data generation when creating.
        """
        progress_report = super().create(validated_data)

        self._generate_report_data(progress_report)

        return progress_report

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["updated_by"] = user

        return super().update(instance, validated_data)

    def _generate_report_data(self, progress_report):
        """
        Handler to progress report data generation
        """

        progress_report_data = {"measure": "value"}  # Example placeholder

        ProgressReportData.objects.create(
            progress_report=progress_report, data=progress_report_data
        )
