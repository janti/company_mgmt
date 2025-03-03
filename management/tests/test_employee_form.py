"""
Employee Form Test Module.

This module contains tests for the employee form functionality.
It follows PEP 8 and PEP 287 standards.

Test Categories:
    - Basic form functionality
    - Special characters (Chinese, Japanese, Arabic)
    - Edge cases (very long strings, infinity values)
    - Form validation
    - CRUD operations
    - Numeric edge cases
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from management.models import Employee, Unit, Company

class EmployeeFormViewTests(TestCase):
    """Test cases for employee form views.

    This class contains test methods for verifying employee form functionality,
    including form rendering, validation, and special character handling.

    Attributes:
        user: A test user instance.
        company: A test company instance.
        unit: A test unit instance.
        employee: A test employee instance.
        url_create: URL for employee creation.
        url_edit: URL for employee editing.
    """
    def setUp(self):
        """Set up test data for all test methods"""
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        # Create a company first
        self.company = Company.objects.create(
            name='Test Company',
            address='123 Test St'
        )

        # Create a unit with company reference
        self.unit = Unit.objects.create(
            name='HR',
            company=self.company
        )

        # Create an employee
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            unit=self.unit
        )

        # Set up URLs
        self.url_create = reverse('employee_create')
        self.url_edit = reverse('employee_edit', args=[self.employee.pk])

    def test_employee_form_view_status_code(self):
        """Test that the employee form view returns a 200 status code"""
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)

    def test_employee_form_view_template_used(self):
        """Test that the employee form view uses the correct template"""
        response = self.client.get(self.url_create)
        self.assertTemplateUsed(response, 'management/employee_form.html')

    def test_employee_form_view_context(self):
        """Test that the employee form view provides the correct context data"""
        response = self.client.get(self.url_create)
        self.assertIn('form', response.context)

    def test_employee_form_view_edit_employee(self):
        """Test that the form view displays the correct header for editing"""
        response = self.client.get(self.url_edit)
        self.assertContains(response, 'Edit Employee')

    def test_employee_form_view_new_employee(self):
        """Test that the form view displays the correct header for creation"""
        response = self.client.get(self.url_create)
        self.assertContains(response, 'New Employee')

    def test_special_case_invalid_form(self):
        """Test the special case where the form is invalid"""
        response = self.client.post(self.url_create, {
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 200)  # Form should return to same page
        self.assertContains(response, 'This field is required')  # Check error message in response
        self.assertContains(response, 'Enter a valid email address')

    def test_special_case_long_names(self):
        """Test the special case where employee names are very long"""
        long_name = 'A' * 100  # Adjust based on your model's max_length
        response = self.client.post(self.url_create, {
            'first_name': long_name,
            'last_name': long_name,
            'email': 'long.name@example.com',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Employee.objects.filter(
                first_name=long_name,
                last_name=long_name
            ).exists()
        )

    def test_special_case_special_characters(self):
        """Test the special case where names contain special characters"""
        special_name = 'Tëst Nämë'
        response = self.client.post(self.url_create, {
            'first_name': special_name,
            'last_name': special_name,
            'email': 'special.name@example.com',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Employee.objects.filter(
                first_name=special_name,
                last_name=special_name
            ).exists()
        )

    def test_special_case_chinese_characters(self):
        """Test the special case where names contain Chinese characters"""
        chinese_name = '张伟'
        response = self.client.post(self.url_create, {
            'first_name': chinese_name,
            'last_name': '李',
            'email': 'chinese.test@example.com',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Employee.objects.filter(
                first_name=chinese_name
            ).exists()
        )

    def test_special_case_japanese_characters(self):
        """Test the special case where names contain Japanese characters"""
        japanese_name = '田中太郎'
        response = self.client.post(self.url_create, {
            'first_name': japanese_name,
            'last_name': '山田花子',
            'email': 'japanese.test@example.com',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Employee.objects.filter(
                first_name=japanese_name
            ).exists()
        )

    def test_special_case_extremely_long_names(self):
        """Test handling of extremely long names (edge case)."""
        very_long_name = 'A' * 1000  # Test with 1000 characters
        response = self.client.post(self.url_create, {
            'first_name': very_long_name,
            'last_name': 'Test',
            'email': 'long.name@example.com',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 200)  # Should stay on form
        self.assertContains(response, 'Ensure this value has at most')

    def test_special_case_arabic_names(self):
        """Test handling of Arabic names and characters."""
        arabic_first_name = 'محمد'  # Mohammed
        arabic_last_name = 'العربي'  # Al-Arabi
        response = self.client.post(self.url_create, {
            'first_name': arabic_first_name,
            'last_name': arabic_last_name,
            'email': 'arabic.test@example.com',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Employee.objects.filter(
                first_name=arabic_first_name,
                last_name=arabic_last_name
            ).exists()
        )

    def test_special_case_infinity_values(self):
        """Test handling of infinity symbols in names."""
        infinity_name = '∞ Employee'
        response = self.client.post(self.url_create, {
            'first_name': infinity_name,
            'last_name': '-∞ Test',
            'email': 'infinity.test@example.com',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Employee.objects.filter(
                first_name=infinity_name
            ).exists()
        )

    def test_mixed_scripts_and_numbers(self):
        """Test handling of mixed scripts with numbers."""
        mixed_name = 'Employee∞ - موظف - 職員'
        response = self.client.post(self.url_create, {
            'first_name': mixed_name,
            'last_name': '123测试',
            'email': 'mixed.test@example.com',
            'unit': self.unit.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Employee.objects.filter(
                first_name=mixed_name
            ).exists()
        )