from django.contrib import admin  # Add this import
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'employee_id', 'department', 'position', 'hours_per_week', 'hourly_salary', 'created_at')
    list_filter = ('department', 'position', 'created_at')
    search_fields = ('first_name', 'last_name', 'employee_id')
    ordering = ('-created_at',)
    fields = ('first_name', 'last_name', 'employee_id', 'address', 'phone_number', 'department', 'position', 'hours_per_week', 'hourly_salary')
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)