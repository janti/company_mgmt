"""
Company Form Test Module.

This module contains tests for the company form functionality.
It follows PEP 8 and PEP 287 standards.

Test Categories:
    - Basic form functionality
    - Special characters (Chinese, Japanese, Arabic)
    - Edge cases (very long strings, infinity values)
    - Form validation
    - CRUD operations
    - Numeric edge cases
    - RTL text support
    - Mixed script handling
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from management.models import Company

class CompanyFormViewTests(TestCase):
    """Test cases for company form views.

    This class contains test methods for verifying company form functionality,
    including form rendering, validation, and special character handling.

    Attributes:
        user: A test user instance.
        company: A test company instance.
        url_create: URL for company creation.
        url_edit: URL for company editing.
    """
    def setUp(self):
        """Set up test data"""
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a company
        self.company = Company.objects.create(name='Test Company', address='123 Test St')
        
        # Set up URLs
        self.url_create = reverse('company_create')
        self.url_edit = reverse('company_edit', args=[self.company.pk])

    def test_company_form_view_status_code(self):
        """Test that the company form view returns a 200 status code."""
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)

    def test_company_form_view_template_used(self):
        """Test that the company form view uses the correct template."""
        response = self.client.get(self.url_create)
        self.assertTemplateUsed(response, 'management/company_form.html')

    def test_company_form_view_context(self):
        """Test that the company form view provides the correct context data."""
        response = self.client.get(self.url_create)
        self.assertIn('form', response.context)

    def test_company_form_view_edit_company(self):
        """Test that the form view displays the correct header for editing."""
        response = self.client.get(self.url_edit)
        self.assertContains(response, 'Edit Company')

    def test_company_form_view_new_company(self):
        """Test that the form view displays the correct header for creation."""
        response = self.client.get(self.url_create)
        self.assertContains(response, 'New Company')

    def test_special_case_invalid_form(self):
        """Test the special case where the form is invalid."""
        response = self.client.post(self.url_create, {
            'name': '',
            'address': ''
        })
        self.assertEqual(response.status_code, 200)  # Form should return to same page
        self.assertContains(response, 'This field is required')

    def test_special_case_long_names(self):
        """Test the special case where company names are very long."""
        long_name = 'A' * 100  # Adjust based on your model's max_length
        response = self.client.post(self.url_create, {
            'name': long_name,
            'address': '123 Test St'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Company.objects.filter(name=long_name).exists())

    def test_special_case_special_characters(self):
        """Test the special case where company names contain special characters."""
        special_name = 'Tëst Cømpåñy'
        response = self.client.post(self.url_create, {
            'name': special_name,
            'address': '123 Test St'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Company.objects.filter(name=special_name).exists())

    def test_special_case_chinese_characters(self):
        """Test the special case where company names contain Chinese characters."""
        chinese_name = '测试公司'
        response = self.client.post(self.url_create, {
            'name': chinese_name,
            'address': '123 Test St'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Company.objects.filter(name=chinese_name).exists())

    def test_successful_company_creation(self):
        """Test successful company creation."""
        response = self.client.post(self.url_create, {
            'name': 'New Company',
            'address': '456 New St'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Company.objects.filter(name='New Company').exists())

    def test_successful_company_edit(self):
        """Test successful company edit."""
        response = self.client.post(self.url_edit, {
            'name': 'Updated Company',
            'address': '789 Edit St'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'Updated Company')

    def test_special_case_extremely_long_string(self):
        """Test handling of extremely long company names."""
        very_long_name = 'A' * 1000  # Test with 1000 characters
        response = self.client.post(self.url_create, {
            'name': very_long_name,
            'address': '123 Test St'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on form
        self.assertContains(response, 'Ensure this value has at most')

    def test_special_case_arabic_text(self):
        """Test handling of Arabic company names and addresses."""
        arabic_name = 'شركة الاختبار'  # Test Company in Arabic
        arabic_address = 'شارع الاختبار ١٢٣'  # Test Street 123 in Arabic
        response = self.client.post(self.url_create, {
            'name': arabic_name,
            'address': arabic_address
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Company.objects.filter(
                name=arabic_name,
                address=arabic_address
            ).exists()
        )

    def test_special_case_infinity_values(self):
        """Test handling of infinity symbols in company names."""
        infinity_name = '∞ Company'
        response = self.client.post(self.url_create, {
            'name': infinity_name,
            'address': '123 ∞ Street'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Company.objects.filter(name=infinity_name).exists())

    def test_special_case_negative_infinity(self):
        """Test handling of negative infinity symbols in company names."""
        neg_infinity_name = '-∞ Corporation'
        response = self.client.post(self.url_create, {
            'name': neg_infinity_name,
            'address': '123 -∞ Avenue'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(Company.objects.filter(name=neg_infinity_name).exists())

    def test_mixed_scripts_and_numbers(self):
        """Test handling of mixed scripts with numbers."""
        mixed_name = 'Company∞ - شركة - 公司'
        mixed_address = '123 Test St, شارع ١٢٣, 测试街123'
        response = self.client.post(self.url_create, {
            'name': mixed_name,
            'address': mixed_address
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(
            Company.objects.filter(
                name=mixed_name,
                address=mixed_address
            ).exists()
        )