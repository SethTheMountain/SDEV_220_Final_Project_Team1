# registration/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import Employee
import json

def main(request):
    """
    Main page view: Displays the homepage with a login form for admins.
    If a POST request is received, attempts to authenticate and log in the user.
    Passes the timezone_set flag to the template to prevent infinite reloads.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('custom_admin')
            else:
                messages.error(request, "You must be an admin to access the dashboard.")
        else:
            messages.error(request, "Invalid username or password.")

    timezone_set = request.session.get('user_timezone') is not None
    return render(request, 'main.html', {'timezone_set': timezone_set})

@require_POST
@ensure_csrf_cookie
def set_timezone(request):
    """
    API view to set the user's timezone in the session.
    Expects a POST request with a JSON body containing the timezone.
    Returns a JSON response indicating success or failure.
    """
    try:
        data = json.loads(request.body)
        timezone = data.get('timezone')
        if timezone:
            request.session['user_timezone'] = timezone
            request.session.modified = True
            return JsonResponse({'status': 'success', 'message': 'Timezone set successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Timezone not provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'}, status=500)

def logout_view(request):
    """
    View to log out the user and clear the timezone from the session.
    Redirects to the main page with a success message.
    """
    logout(request)
    if 'user_timezone' in request.session:
        del request.session['user_timezone']
    messages.success(request, "You have been logged out successfully.")
    return redirect('main')

def register(request):
    """
    View to handle employee registration.
    Validates form data, creates a new Employee instance, and redirects to the confirmation page.
    """
    if request.method == 'POST':
        try:
            form_data = {
                'first_name': request.POST.get('first_name', '').strip(),
                'last_name': request.POST.get('last_name', '').strip(),
                'employee_id': request.POST.get('employee_id', '').strip(),
                'address': request.POST.get('address', '').strip(),
                'phone_number': request.POST.get('phone_number', '').strip(),
                'department': request.POST.get('department', '').strip(),
                'position': request.POST.get('position', '').strip(),
                'hours_per_week': request.POST.get('hours_per_week', ''),
                'hourly_salary': request.POST.get('hourly_salary', ''),
            }

            if not form_data['first_name'].isalpha() or not form_data['last_name'].isalpha():
                messages.error(request, "First and last names must contain only letters.")
                return render(request, 'register.html', {'form_data': form_data})

            if not form_data['phone_number'].replace('-', '').isdigit() or len(form_data['phone_number']) != 12:
                messages.error(request, "Phone number must be in the format 111-111-1111.")
                return render(request, 'register.html', {'form_data': form_data})

            if Employee.objects.filter(employee_id=form_data['employee_id']).exists():
                messages.error(request, "Employee ID must be unique.")
                return render(request, 'register.html', {'form_data': form_data})

            employee = Employee(
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                employee_id=form_data['employee_id'],
                address=form_data['address'],
                phone_number=form_data['phone_number'],
                department=form_data['department'],
                position=form_data['position'],
                hours_per_week=float(form_data['hours_per_week']),
                hourly_salary=float(form_data['hourly_salary'])
            )
            employee.save()

            messages.success(request, "Employee registered successfully.")
            return redirect('confirmation')
        except ValueError as e:
            messages.error(request, f"Invalid input: {str(e)}")
            return render(request, 'register.html', {'form_data': form_data})
        except Exception as e:
            messages.error(request, f"Error registering employee: {str(e)}")
            return render(request, 'register.html', {'form_data': form_data})
    return render(request, 'register.html')

def confirmation(request):
    """View to display the registration confirmation page."""
    return render(request, 'confirmation.html')

@login_required(login_url='main')
@user_passes_test(lambda u: u.is_superuser, login_url='main')
def custom_admin(request):
    """
    Admin dashboard view: Displays all registered employees.
    Accessible only to authenticated superusers.
    """
    employees = Employee.objects.all()
    return render(request, 'custom_admin.html', {'employees': employees})

@login_required(login_url='main')
@user_passes_test(lambda u: u.is_superuser, login_url='main')
def edit_employee(request, employee_id):
    """
    View to edit an employee's details.
    Validates form data, updates the employee record, and redirects to the admin dashboard.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        try:
            form_data = {
                'first_name': request.POST.get('first_name', '').strip(),
                'last_name': request.POST.get('last_name', '').strip(),
                'employee_id': request.POST.get('employee_id', '').strip(),
                'address': request.POST.get('address', '').strip(),
                'phone_number': request.POST.get('phone_number', '').strip(),
                'department': request.POST.get('department', '').strip(),
                'position': request.POST.get('position', '').strip(),
                'hours_per_week': request.POST.get('hours_per_week', ''),
                'hourly_salary': request.POST.get('hourly_salary', ''),
            }

            if not form_data['first_name'].isalpha() or not form_data['last_name'].isalpha():
                messages.error(request, "First and last names must contain only letters.")
                return render(request, 'edit_employee.html', {'employee': employee, 'form_data': form_data})

            if not form_data['phone_number'].replace('-', '').isdigit() or len(form_data['phone_number']) != 12:
                messages.error(request, "Phone number must be in the format 111-111-1111.")
                return render(request, 'edit_employee.html', {'employee': employee, 'form_data': form_data})

            if Employee.objects.filter(employee_id=form_data['employee_id']).exclude(id=employee_id).exists():
                messages.error(request, "Employee ID must be unique.")
                return render(request, 'edit_employee.html', {'employee': employee, 'form_data': form_data})

            employee.first_name = form_data['first_name']
            employee.last_name = form_data['last_name']
            employee.employee_id = form_data['employee_id']
            employee.address = form_data['address']
            employee.phone_number = form_data['phone_number']
            employee.department = form_data['department']
            employee.position = form_data['position']
            employee.hours_per_week = float(form_data['hours_per_week'])
            employee.hourly_salary = float(form_data['hourly_salary'])

            employee.save()
            messages.success(request, "Employee updated successfully.")
            return redirect('custom_admin')
        except ValueError as e:
            messages.error(request, f"Invalid input: {str(e)}")
            return render(request, 'edit_employee.html', {'employee': employee, 'form_data': form_data})
        except Exception as e:
            messages.error(request, f"Error updating employee: {str(e)}")
            return render(request, 'edit_employee.html', {'employee': employee, 'form_data': form_data})
    return render(request, 'edit_employee.html', {'employee': employee})

@login_required(login_url='main')
@user_passes_test(lambda u: u.is_superuser, login_url='main')
def delete_employee(request, employee_id):
    """
    View to delete an employee record.
    Deletes the employee and redirects to the admin dashboard.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    messages.success(request, "Employee deleted successfully.")
    return redirect('custom_admin')

@login_required(login_url='main')
@user_passes_test(lambda u: u.is_superuser, login_url='main')
@require_POST
def update_employee(request, employee_id):
    """
    View to update an employee record from the block-based form.
    Validates form data, updates the employee, and redirects to the admin dashboard.
    """
    employee = get_object_or_404(Employee, id=employee_id)

    try:
        form_data = {
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'employee_id': request.POST.get('employee_id', '').strip(),
            'address': request.POST.get('address', employee.address),
            'phone_number': request.POST.get('phone_number', employee.phone_number),
            'department': request.POST.get('department', '').strip(),
            'position': request.POST.get('position', '').strip(),
            'hours_per_week': request.POST.get('hours_per_week', ''),
            'hourly_salary': request.POST.get('hourly_salary', ''),
        }

        # Validation
        if not form_data['first_name'].isalpha() or not form_data['last_name'].isalpha():
            messages.error(request, "First and last names must contain only letters.")
            return redirect('custom_admin')

        if not form_data['phone_number'].replace('-', '').isdigit() or len(form_data['phone_number']) != 12:
            messages.error(request, "Phone number must be in the format 111-111-1111.")
            return redirect('custom_admin')

        if Employee.objects.filter(employee_id=form_data['employee_id']).exclude(id=employee_id).exists():
            messages.error(request, "Employee ID must be unique.")
            return redirect('custom_admin')

        # Update employee fields
        employee.first_name = form_data['first_name']
        employee.last_name = form_data['last_name']
        employee.employee_id = form_data['employee_id']
        employee.address = form_data['address']
        employee.phone_number = form_data['phone_number']
        employee.department = form_data['department']
        employee.position = form_data['position']
        employee.hours_per_week = float(form_data['hours_per_week'])
        employee.hourly_salary = float(form_data['hourly_salary'])

        employee.save()
        messages.success(request, f"Employee {employee.first_name} {employee.last_name} updated successfully!")
        return redirect('custom_admin')

    except ValueError as e:
        messages.error(request, f"Invalid input: {str(e)}")
        return redirect('custom_admin')
    except Exception as e:
        messages.error(request, f"Error updating employee: {str(e)}")
        return redirect('custom_admin')