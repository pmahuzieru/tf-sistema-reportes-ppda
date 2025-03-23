from django.contrib import admin
from reporting.models import ProgressReport

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