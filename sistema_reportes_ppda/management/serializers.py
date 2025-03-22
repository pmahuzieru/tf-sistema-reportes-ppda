from rest_framework import serializers
from management.models import EnvironmentalPlan, Measure, MeasureReport, ReportFile, Body,BodyMeasure
    

class ReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFile
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)
    

class MeasureReportSerializer(serializers.ModelSerializer):
    files = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='file-detail')
    
    class Meta:
        model = MeasureReport
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)


class MeasureSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Body
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)

class BodyMeasureSerializer(serializers.ModelSerializer):
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