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