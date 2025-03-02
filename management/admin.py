from django.contrib import admin
from .models import Company, Unit, Employee

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'unit')
