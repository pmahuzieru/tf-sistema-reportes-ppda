from django.contrib import admin
from accounts.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "rut", "is_staff", "is_active")
