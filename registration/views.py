# registration/views.py
from django.shortcuts import render, redirect
from .models import Employee
from django.contrib import messages

def main_view(request):
    return render(request, 'main.html')

def register_view(request):
    if request.method == 'POST':
        try:
            employee = Employee(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                employee_id=request.POST['employee_id'],
                address=request.POST['address'],
                phone_number=request.POST['phone_number'],
                position=request.POST['position'],
                department=request.POST['department'],
                hours_per_week=float(request.POST['hours_per_week']),
                hourly_salary=request.POST['hourly_salary']
            )
            employee.save()
            return redirect('confirmation')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, 'register.html')

def confirmation_view(request):
    return render(request, 'confirmation.html')