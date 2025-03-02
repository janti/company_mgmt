from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('companies/', views.company_list, name='company_list'),
    path('company/new/', views.company_edit, name='company_create'),
    path('company/edit/<int:pk>/', views.company_edit, name='company_edit'),

    path('units/', views.unit_list, name='unit_list'),
    path('unit/new/', views.unit_edit, name='unit_create'),
    path('unit/edit/<int:pk>/', views.unit_edit, name='unit_edit'),

    path('employees/', views.employee_list, name='employee_list'),
    path('employee/new/', views.employee_edit, name='employee_create'),
    path('employee/edit/<int:pk>/', views.employee_edit, name='employee_edit'),
]
