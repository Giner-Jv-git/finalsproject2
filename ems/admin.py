from django.contrib import admin
from .models import Department, Position, Employee, Attendance, LeaveRequest

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'department', 'position', 'is_active')
    list_filter = ('department', 'position', 'is_active')
    search_fields = ('first_name', 'last_name', 'employee_id', 'email')
    list_per_page = 20

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'check_in', 'check_out')
    list_filter = ('status', 'date')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    date_hierarchy = 'date'
    list_per_page = 20

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'leave_type', 'start_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_id')
    date_hierarchy = 'start_date'
    list_per_page = 20

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)