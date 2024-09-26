from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError
from HandymanHive.models import Service

class ServiceModelTest(TestCase):

  def setUp(self):
    self.valid_data = {
      'name': "Web Development",
      'description': "This service includes creating websites and web applications.",
    }

  def test_create_valid_service(self):
    """Tests creating a Service object with valid data"""
    service = Service.objects.create(**self.valid_data)
    # assert object creation and field values
    self.assertEqual(service.name, self.valid_data['name'])
    self.assertEqual(service.description, self.valid_data['description'])

  def test_create_service_with_empty_description(self):
    """Tests creating a Service object with an empty description"""
    empty_data = self.valid_data.copy()
    empty_data['description'] = ""
    service = Service.objects.create(**empty_data)
    self.assertEqual(service.description, "")  # Check if it's an empty string

  def test_create_service_with_too_long_name(self):
    """Tests exceeding max length for name"""
    invalid_data = self.valid_data.copy()
    invalid_data['name'] = "x" * 51  # String longer than max length
    with self.assertRaises(DataError):
      Service.objects.create(**invalid_data)

  def test_unique_name_constraint(self):
    """Tests creating a duplicate Service (enforces unique name)"""
    service1 = Service.objects.create(**self.valid_data)
    with self.assertRaises(IntegrityError):
      Service.objects.create(**self.valid_data)  # Duplicate data

  def test_str_method_output(self):
    """Tests the __str__ method output"""
    service = Service.objects.create(**self.valid_data)
    self.assertEqual(str(service), self.valid_data['name'])

# (Optional) Add tests for database interactions using fixtures
