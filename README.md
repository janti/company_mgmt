# Company Management System

## Overview
A Django-based company management system for handling companies, units, and employees.

## Project Structure
```
company_mgmt/
├── management/
│   ├── templates/
│   │   └── management/
│   │       ├── company_form.html
│   │       ├── unit_form.html
│   │       └── employee_form.html
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_company_form.py
│   │   ├── test_unit_form.py
│   │   └── test_employee_form.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── manage.py
└── README.md
```

## Installation
1. Clone the repository
2. Create a virtual environment
3. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Testing
Run the test suite:
```bash
python manage.py test management.tests
```

## Documentation

### Models
- `Company`: Represents a company with name and address
- `Unit`: Represents a unit within a company
- `Employee`: Represents an employee within a unit

### Test Files

#### test_company_form.py
Tests for company form functionality including:
- Form rendering
- Form validation
- Special character handling
- Unicode support

#### test_unit_form.py
Tests for unit form functionality including:
- Form rendering
- Form validation
- Company relationships
- Special character handling

#### test_employee_form.py
Tests for employee form functionality including:
- Form rendering
- Form validation
- Unit relationships
- Special character handling

## Standards
This project follows:
- PEP 8 (Style Guide for Python Code)
- PEP 257 (Docstring Conventions)
- PEP 287 (reStructuredText Docstring Format)

# Company Management System Tests

## Special Character Support

The system supports various character sets and special cases:
- Arabic text (RTL): قسم الموارد البشرية
- Chinese characters: 人力资源部
- Japanese characters: 人事部
- Special symbols: ∞, -∞
- Mixed scripts: HR部門 - قسم 人力资源
- Very long strings (tested up to 1000 characters)

## Edge Cases Tested
- Maximum length validation
- Special character handling
- Right-to-left text
- Mixed script text
- Unicode symbols
- Extremely long input strings

## Running Tests

```bash
python manage.py test management.tests.test_unit_form -v 2
```

## Test Categories

1. Basic Form Operations
   - Form rendering
   - Template usage
   - Context data

2. Unicode Support
   - Arabic text
   - Chinese characters
   - Japanese characters
   - Mixed scripts

3. Edge Cases
   - Very long strings
   - Infinity symbols
   - Special characters
   - Maximum length validation

4. Form Validation
   - Required fields
   - Field length limits
   - Character encoding

5. Database Integrity
   - Creation verification
   - Update verification
   - Special character storage

# Employee Management System Tests

## Edge Cases and Special Characters

### Character Support
- Arabic text (RTL): محمد العربي
- Chinese characters: 张伟
- Japanese characters: 田中太郎
- Special symbols: ∞, -∞
- Mixed scripts: Employee∞ - موظف - 職員
- Numeric values in names: 123测试
- Very long strings (1000+ characters)

### Test Categories
1. Basic Form Operations
   - Form rendering
   - Template usage
   - Context data

2. Unicode Support
   - Right-to-left (Arabic) text
   - Chinese characters
   - Japanese characters
   - Mixed script support

3. Edge Cases
   - Extremely long strings (1000+ chars)
   - Infinity symbols (∞, -∞)
   - Mixed scripts with numbers
   - Maximum length validation

4. Form Validation
   - Required fields
   - Email format
   - Field length limits
   - Character encoding

5. Database Integrity
   - Creation verification
   - Update verification
   - Special character storage
   - Unicode handling

## Running Tests
```bash
cd c:\koodaus\company_mgmt
python manage.py test management.tests.test_employee_form -v 2
```

## Test Coverage
Tests cover:
- Form rendering and validation
- Unicode character handling
- Edge cases with long strings
- Special character storage
- Mixed script support
- RTL text handling

# Company Management System Tests

## Edge Cases and Special Characters Support

### Character Support
- Arabic text (RTL): شركة الاختبار
- Chinese characters: 测试公司
- Special symbols: ∞, -∞
- Mixed scripts: Company∞ - شركة - 公司
- Numeric values: ١٢٣
- Very long strings (1000+ characters)

### Test Categories
1. Basic Form Operations
   - Form rendering
   - Template usage
   - Context data

2. Unicode Support
   - Right-to-left (Arabic) text
   - Chinese characters
   - Mixed script support
   - Special symbols

3. Edge Cases
   - Extremely long strings (1000+ chars)
   - Infinity symbols (∞, -∞)
   - Mixed scripts with numbers
   - Maximum length validation

4. Form Validation
   - Required fields
   - Field length limits
   - Character encoding

5. Database Integrity
   - Creation verification
   - Update verification
   - Special character storage
   - Unicode handling

## Running Tests
```bash
cd c:\koodaus\company_mgmt
python manage.py test management.tests.test_company_form -v 2
```