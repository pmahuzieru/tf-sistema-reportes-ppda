from django.utils.timezone import localtime
from rest_framework import serializers
from reporting.models import ProgressReport, ProgressReportData

from management.models import Measure, MeasureReport, EnvironmentalPlan


class ProgressReportSerializer(serializers.ModelSerializer):
    environmental_plan_id = serializers.PrimaryKeyRelatedField(
        source='environmental_plan',
        queryset=EnvironmentalPlan.objects.all(),
        write_only=True
    )
    environmental_plan = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='environmentalplan-detail'
    )
    

    class Meta:
        model = ProgressReport
        fields = "__all__"
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]

    def create(self, validated_data):
        """
        Will trigger Progress Report Data generation when creating.
        """
        user = self.context["request"].user
        validated_data["created_by"] = user
        
        progress_report = super().create(validated_data)

        try:
            self._generate_report_data(progress_report)
            progress_report.data_created = True
            progress_report.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error generating report data: {str(e)}")

        return progress_report

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["updated_by"] = user

        return super().update(instance, validated_data)

    def _generate_report_data(self, progress_report):
        """
        Generates report data
        """

        environmental_plan = progress_report.environmental_plan
        measures = Measure.objects.filter(reference_PDA=environmental_plan)

        measure_data = {}  # Keys are Measure IDs

        for measure in measures:
            # Get the latest report on the measure
            latest_report = (
                MeasureReport.objects.filter(measure=measure)
                .order_by("-created_at")
                .first()
            )
            
            if latest_report:
                measure_data[str(measure.id)] = {
                    "measure_short_name": measure.short_name,
                    "reported_value": latest_report.reported_value,
                    "reported_at": localtime(latest_report.created_at).isoformat(),
                }
            else:
                measure_data[str(measure.id)] = {
                    "measure_short_name": measure.short_name,
                    "reported_value": None,
                    "reported_at": None,
                }  

        ProgressReportData.objects.create(
            progress_report=progress_report, data=measure_data
        )
