from rest_framework import serializers
from reporting.models import ProgressReport
from reporting.services.progress_report_data_generator import ProgressReportDataGenerator

from management.models import EnvironmentalPlan


class ProgressReportSerializer(serializers.ModelSerializer):
    
    # For 'writing' operations, you pass the ID in the payload/body.
    environmental_plan_id = serializers.PrimaryKeyRelatedField(
        source='environmental_plan',
        queryset=EnvironmentalPlan.objects.all(),
        write_only=True
    )
    
    # For 'read' operations, returns the hyperlink to the resource.
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
            ProgressReportDataGenerator(progress_report).generate()
            progress_report.data_created = True
            progress_report.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error generating report data: {str(e)}")

        return progress_report

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["updated_by"] = user

        return super().update(instance, validated_data)
