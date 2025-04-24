from django.contrib import admin
from django.utils.html import format_html
from reporting.models import ProgressReport, ProgressReportData
import json

@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'environmental_plan', 'created_at')
    search_fields = ('name',)    
    readonly_fields = ('created_at', 'created_by', 'updated_at',  'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(ProgressReportData)
class ProgressReportDataAdmin(admin.ModelAdmin):
    list_display = ('progress_report', 'created_at', 'updated_at', 'shortened_data')
    search_fields = ['progress_report__name']
    readonly_fields = ('progress_report', 'created_at', 'updated_at', 'formatted_data')
    
    def shortened_data(self, obj):
        # Return a truncated version of the JSON data to avoid overloading the admin interface
        data_str = json.dumps(obj.data, indent=2)
        return format_html('<pre>{}</pre>', data_str[:100])  # Display the first 200 chars of the JSON
    
    def formatted_data(self, obj):
        # This method will display the full formatted JSON in a read-only field.
        return format_html('<pre>{}</pre>', json.dumps(obj.data, indent=2))

    shortened_data.short_description = "JSON Data (Truncated)"
    formatted_data.short_description = "Formatted JSON Data"