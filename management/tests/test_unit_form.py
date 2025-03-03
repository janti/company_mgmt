"""
Unit Form Test Module.

This module contains tests for the unit form functionality.
It follows PEP 8 and PEP 287 standards.

Classes:
    UnitFormViewTests: Test cases for unit form views.

Test Cases:
    - Basic form functionality
    - Special characters (Chinese, Japanese, Arabic)
    - Edge cases (very long strings, infinity values)
    - Form validation
    - CRUD operations
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from management.models import Unit, Company

class UnitFormViewTests(TestCase):
    """Test cases for unit form views.

    This class contains test methods for verifying unit form functionality,
    including form rendering, validation, and special character handling.

    Attributes:
        user: A test user instance.
        company: A test company instance.
        unit: A test unit instance.
        url_create: URL for unit creation.
        url_edit: URL for unit editing.

    Test Categories:
        - Basic form operations
        - Unicode character support
        - Edge cases
        - Form validation
        - Database integrity
    """
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        cls.client = Client()
        # Create test user
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Create a company first
        cls.company = Company.objects.create(
            name='Test Company',
            address='123 Test St'
        )
        # Create unit with company reference
        cls.unit = Unit.objects.create(
            name='HR',
            company=cls.company
        )
        # Set up URLs
        cls.url_create = reverse('unit_create')
        cls.url_edit = reverse('unit_edit', args=[cls.unit.pk])

    def setUp(self):
        """Set up test case specific data"""
        self.client.login(username='testuser', password='testpassword')

    def test_unit_form_view_status_code(self):
        """Test that the unit form view returns a 200 status code"""
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)

    def test_unit_form_view_template_used(self):
        """Test that the unit form view uses the correct template"""
        response = self.client.get(self.url_create)
        self.assertTemplateUsed(response, 'management/unit_form.html')

    def test_unit_form_view_context(self):
        """Test that the unit form view provides the correct context data"""
        response = self.client.get(self.url_create)
        self.assertIn('form', response.context)

    def test_unit_form_view_edit_unit(self):
        """Test that the unit form view displays the correct header for editing a unit"""
        response = self.client.get(self.url_edit)
        self.assertContains(response, 'Edit Unit')

    def test_unit_form_view_new_unit(self):
        """Test that the unit form view displays the correct header for creating a new unit"""
        response = self.client.get(self.url_create)
        self.assertContains(response, 'New Unit')

    def test_special_case_invalid_form(self):
        """Test the special case where the form is invalid"""
        response = self.client.post(self.url_create, {
            'name': '',
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 200)  # Form should return to the same page
        self.assertContains(response, 'This field is required')

    def test_special_case_long_names(self):
        """Test the special case where unit names are very long"""
        # Adjust length based on your model's max_length
        long_name = 'A' * 100
        response = self.client.post(self.url_create, {
            'name': long_name,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Unit.objects.filter(name=long_name).exists())

    def test_special_case_special_characters(self):
        """Test the special case where unit names contain special characters"""
        special_name = 'Tëst Ünît'
        response = self.client.post(self.url_create, {
            'name': special_name,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Unit.objects.filter(name=special_name).exists())

    def test_special_case_chinese_characters(self):
        """Test the special case where unit names contain Chinese characters"""
        chinese_name = '测试单位'
        response = self.client.post(self.url_create, {
            'name': chinese_name,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Unit.objects.filter(name=chinese_name).exists())

    def test_unit_form_view_successful_creation(self):
        """Test successful unit creation"""
        response = self.client.post(self.url_create, {
            'name': 'New Unit',
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Unit.objects.filter(name='New Unit').exists())

    def test_unit_form_view_successful_edit(self):
        """Test successful unit edit"""
        response = self.client.post(self.url_edit, {
            'name': 'Updated HR',
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.unit.refresh_from_db()
        self.assertEqual(self.unit.name, 'Updated HR')

    def test_special_case_very_long_string(self):
        """Test the special case where unit names are extremely long."""
        very_long_name = 'A' * 1000  # Try with 1000 characters
        response = self.client.post(self.url_create, {
            'name': very_long_name,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 200)  # Should return to form
        self.assertContains(response, 'Ensure this value has at most')

    def test_special_case_infinity(self):
        """Test the special case where unit names contain infinity symbols."""
        infinity_name = '∞ Department'  # Unicode infinity symbol
        response = self.client.post(self.url_create, {
            'name': infinity_name,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Unit.objects.filter(name=infinity_name).exists())

    def test_special_case_negative_infinity(self):
        """Test the special case where unit names contain negative infinity symbols."""
        neg_infinity_name = '-∞ Division'  # Negative infinity
        response = self.client.post(self.url_create, {
            'name': neg_infinity_name,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Unit.objects.filter(name=neg_infinity_name).exists())

    def test_special_case_arabic_characters(self):
        """Test the special case where unit names contain Arabic characters."""
        arabic_name = 'قسم الموارد البشرية'  # Human Resources Department in Arabic
        response = self.client.post(self.url_create, {
            'name': arabic_name,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Unit.objects.filter(name=arabic_name).exists())

    def test_special_case_mixed_scripts(self):
        """Test the special case where unit names contain mixed scripts."""
        mixed_name = 'HR部門 - قسم 人力资源'  # HR Department in multiple scripts
        response = self.client.post(self.url_create, {
            'name': mixed_name,
            'company': self.company.pk
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Unit.objects.filter(name=mixed_name).exists())