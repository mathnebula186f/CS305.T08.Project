from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError
from datetime import datetime
from django.utils import timezone
from HandymanHive.models import Certification

class CertificationModelTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'certificate_name': "My Certification",
            'worker_email': "test@example.com",
            'issuing_authority': "Some Authority",
            'certificate_data': b"This is some binary data"  # Example binary data
        }

    def test_create_valid_certification(self):
        """Tests creating a Certification object with valid data"""
        cert = Certification.objects.create(**self.valid_data)
        # assert object creation and field values
        self.assertEqual(cert.certificate_name, self.valid_data['certificate_name'])
        self.assertEqual(cert.worker_email, self.valid_data['worker_email'])
        self.assertEqual(cert.issuing_authority, self.valid_data['issuing_authority'])
        self.assertEqual(cert.status, "Pending")
        # assert created_on is set
        self.assertLessEqual(cert.created_on, timezone.now())

    def test_create_invalid_email(self):
        """Tests creating a Certification object with invalid email"""
        invalid_data = self.valid_data.copy()
        invalid_data['worker_email'] = "johndoeexample.com"
        with self.assertRaises(ValidationError):
            Certification.objects.create(**invalid_data)
            
        invalid_data['worker_email'] = "johndoe@"
        with self.assertRaises(ValidationError):
            Certification.objects.create(**invalid_data)
            
        invalid_data['worker_email'] = "johndoe@invaliddomain"
        with self.assertRaises(ValidationError):
            Certification.objects.create(**invalid_data)

    def test_certificate_name_max_length(self):
        """Tests exceeding max length for certificate_name"""
        invalid_data = self.valid_data.copy()
        invalid_data['certificate_name'] = "x" * 256  # String longer than max length
        with self.assertRaises(DataError):
            Certification.objects.create(**invalid_data)

    def test_issuing_authority_max_length(self):
        """Tests exceeding max length for issuing_authority"""
        invalid_data = self.valid_data.copy()
        invalid_data['issuing_authority'] = "x" * 256  # String longer than max length
        with self.assertRaises(DataError):
            Certification.objects.create(**invalid_data)

    def test_optional_certificate_data_type(self):
        """Tests creating a Certification with non-binary certificate_data"""
        invalid_data = self.valid_data.copy()
        invalid_data['certificate_data'] = "This is not binary data"  # String instead of binary
        try:
            Certification.objects.create(**invalid_data)
        except TypeError as e:
            self.assertEqual(str(e), "can't escape str to binary")

      
    def test_str_method_output(self):
        """Tests the __str__ method output"""
        cert = Certification.objects.create(**self.valid_data)
        self.assertEqual(str(cert), self.valid_data['certificate_name'])
