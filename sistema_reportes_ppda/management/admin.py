from django.contrib import admin
from management.models import EnvironmentalPlan, Measure


@admin.register(EnvironmentalPlan)
class EnvironmentalPlanAdmin(admin.ModelAdmin):
    list_display = list_display = ('name', 'type', 'updated_at', 'updated_by')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'created_at', 'created_by', 'updated_at', 'updated_by')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'measure_type', 'created_at', 'created_by', 'updated_at', 'updated_by')
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)