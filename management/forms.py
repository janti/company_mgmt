from django import forms
from .models import Company, Unit, Employee

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address']

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'company']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'unit']
