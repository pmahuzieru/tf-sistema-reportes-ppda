from rest_framework import serializers
from management.models import EnvironmentalPlan, Measure


class EnvironmentalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalPlan
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']
        
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user
        
        return super().update(instance, validated_data)
    

class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)