from rest_framework import serializers
from management.models import EnvironmentalPlan, Measure, MeasureReport, ReportFile, Body,BodyMeasure
from management.utils import parse_boolean, parse_decimal, parse_integer, parse_percentage
    

class ReportFileSerializer(serializers.ModelSerializer):
    """
    Implements tracking of who/when created/updated a ReportFile instance.
    """
    
    class Meta:
        model = ReportFile
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)
    

class MeasureReportSerializer(serializers.ModelSerializer):
    """
    Deserializes MeasureReport inputs, with a main task of validating the type of 
    value being reported.
    Serializes related ReportFiles as hyperlinks (HATEOAS) for read actions.
    Implements tracking of who/when created/updated a MeasureReport instance.
    """
    
    files = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='file-detail')
    
    class Meta:
        model = MeasureReport
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)
    
    def validate_reported_value(self, value):
        """
        Validates that the value reported is consistent with the measure's type of indicator.
        """
        
        measure_id = self.initial_data.get('measure')
        measure = Measure.objects.get(id=measure_id)
        
        measure_value_type = measure.value_type
        
        if measure_value_type == 'boolean':
            return parse_boolean(value)
        if measure_value_type == 'integer':
            return parse_integer(value)
        if measure_value_type == 'decimal':
            return parse_decimal(value)
        if measure_value_type == 'percentage':
            return parse_percentage(value)
        
        return value


class MeasureSerializer(serializers.ModelSerializer):
    """
    Serializes related MeasureReports as hyperlinks (HATEOAS) for read actions.
    Implements tracking of who/when created/updated a MeasureReport instance.
    """
    measure_reports = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='report-detail')
    class Meta:
        model = Measure
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)
 
 
class EnvironmentalPlanSerializer(serializers.ModelSerializer):
    """
    Serializes related Measures as hyperlinks (HATEOAS) for read actions.
    Implements tracking of who/when created/updated a MeasureReport instance.    
    """
    
    measures = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='measure-detail')
    
    class Meta:
        model = EnvironmentalPlan
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']
        
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user
        
        return super().update(instance, validated_data)
    

class BodySerializer(serializers.ModelSerializer):
    """
    Implements tracking of who/when created/updated a Body instance.    
    """
    
    class Meta:
        model = Body
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)

class BodyMeasureSerializer(serializers.ModelSerializer):
    """
    Implements tracking of who/when created/updated a Body instance.    
    """
    
    fk_measure = serializers.PrimaryKeyRelatedField(queryset=Measure.objects.all())
    fk_body = serializers.PrimaryKeyRelatedField(queryset=Body.objects.all())

    class Meta:
        model = BodyMeasure
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']
        
    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)