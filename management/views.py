from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Unit, Employee
from .forms import CompanyForm, UnitForm, EmployeeForm

def home(request):
    return render(request, 'management/home.html')

# Company Views
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'management/companies.html', {'companies': companies})

def company_edit(request, pk=None):
    company = get_object_or_404(Company, pk=pk) if pk else None
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'management/company_form.html', {'form': form})

# Unit Views
def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'management/units.html', {'units': units})

def unit_edit(request, pk=None):
    unit = get_object_or_404(Unit, pk=pk) if pk else None
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'management/unit_form.html', {'form': form})

# Employee Views
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'management/employees.html', {'employees': employees})

def employee_edit(request, pk=None):
    employee = get_object_or_404(Employee, pk=pk) if pk else None
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'management/employee_form.html', {'form': form})
