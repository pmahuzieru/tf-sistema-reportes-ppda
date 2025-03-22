from django.contrib import admin
from management.models import BodyMeasure, EnvironmentalPlan, Measure, MeasureReport, ReportFile, Body


@admin.register(EnvironmentalPlan)
class EnvironmentalPlanAdmin(admin.ModelAdmin):
    list_display = list_display = ('name', 'type', 'updated_at', 'updated_by')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'short_name', 'type', 'created_at', 'created_by', 'updated_at', 'updated_by')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'reference_PDA', 'created_at', 'created_by', 'updated_at', 'updated_by')
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(MeasureReport)
class MeasureReportAdmin(admin.ModelAdmin):
    list_display = ('measure', 'reported_value', 'created_at', 'created_by', 'updated_at', 'updated_by')
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)   
    
@admin.register(ReportFile)
class ReportFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'report', 'created_at', 'created_by', 'updated_at', 'updated_by')
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)   

@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by', 'updated_at', 'updated_by')
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(BodyMeasure)
class BodyMeasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_measure', 'fk_body', 'is_reporter', 'active', 'updated_at', 'updated_by')
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)      
