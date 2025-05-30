from django import forms
from .models import Department, Position, Employee, Attendance, LeaveRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}),
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'department', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 'email', 'phone', 'address',
            'gender', 'date_of_birth', 'department', 'position', 'salary',
            'hire_date', 'profile_picture', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'check_in', 'check_out', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in': forms.TimeInput(attrs={'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}),
        }

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}),
        }

class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}),
        }

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']