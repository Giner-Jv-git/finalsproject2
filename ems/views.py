from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from .models import Department, Position, Employee, Attendance, LeaveRequest
from .forms import (
    DepartmentForm, PositionForm, EmployeeForm, 
    AttendanceForm, LeaveRequestForm, LeaveApprovalForm,
    UserCreateForm
)


def dashboard(request):
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(is_active=True).count()
    departments = Department.objects.annotate(employee_count=Count('employee'))
    recent_employees = Employee.objects.order_by('-hire_date')[:5]
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'departments': departments,
        'recent_employees': recent_employees,
        'pending_leaves': pending_leaves,
    }
    return render(request, 'dashboard.html', context)

# Department Views

def department_list(request):
    departments = Department.objects.annotate(employee_count=Count('employee'))
    return render(request, 'departments/list.html', {'departments': departments})


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/form.html', {'form': form, 'title': 'Create Department'})


def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/form.html', {'form': form, 'title': 'Edit Department'})


def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('department_list')
    return render(request, 'departments/delete.html', {'department': department})

# Employee Views

def employee_list(request):
    employees = Employee.objects.select_related('department', 'position')
    return render(request, 'employees/list.html', {'employees': employees})


def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee created successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/form.html', {'form': form, 'title': 'Create Employee'})


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/detail.html', {'employee': employee})


def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit Employee'})


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employee_list')
    return render(request, 'employees/delete.html', {'employee': employee})

# Attendance Views

def attendance_list(request):
    attendances = Attendance.objects.select_related('employee').order_by('-date')
    return render(request, 'attendance/list.html', {'attendances': attendances})

def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.created_by = request.user
            attendance.save()
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/form.html', {'form': form, 'title': 'Record Attendance'})

# Leave Request Views

def leave_list(request):
    if request.user.is_superuser:
        leaves = LeaveRequest.objects.select_related('employee').order_by('-start_date')
    else:
        employee = request.user.employee
        leaves = LeaveRequest.objects.filter(employee=employee).order_by('-start_date')
    return render(request, 'leave/list.html', {'leaves': leaves})


def leave_create(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user.employee
            leave.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/form.html', {'form': form, 'title': 'Request Leave'})


def leave_detail(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST' and request.user.is_superuser:
        form = LeaveApprovalForm(request.POST, instance=leave)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.approved_by = request.user
            leave.save()
            messages.success(request, 'Leave request updated successfully!')
            return redirect('leave_list')
    else:
        form = LeaveApprovalForm(instance=leave)
    return render(request, 'leave/detail.html', {'leave': leave, 'form': form})

# User Management

def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreateForm()
    return render(request, 'registration/user_form.html', {'form': form})