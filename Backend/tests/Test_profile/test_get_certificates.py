import json
import base64
from django.test import TestCase
from django.urls import reverse
from HandymanHive.models import Certification

class GetCertificatesTestCase(TestCase):
    def setUp(self):
        # Create sample data for testing
        certificate_data = "Data 1"
        encoded_certificate_data = base64.b64encode(certificate_data.encode())
        Certification.objects.create(
            certificate_name="Certificate 1",
            issuing_authority="Authority 1",
            certificate_data=encoded_certificate_data,
            worker_email="test@example.com",
            status="Active"
        )

    def test_invalid_request_method(self):
        response = self.client.get(reverse('get_certificates'))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request method", response.json().get("error"))

    def test_valid_post_request_certificates_found(self):
        data = {"email": "test@example.com"}
        response = self.client.post(reverse('get_certificates'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        certificates = response.json().get("certificates")
        self.assertEqual(len(certificates), 1)
        self.assertEqual(certificates[0]["certificate_name"], "Certificate 1")

    def test_valid_post_request_no_certificates_found(self):
        data = {"email": "notfound@example.com"}
        response = self.client.post(reverse('get_certificates'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        certificates = response.json().get("certificates")
        self.assertEqual(len(certificates), 0)

    def test_valid_post_request_with_correct_data(self):
        data = {"email": "test@example.com"}
        response = self.client.post(reverse('get_certificates'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        certificates = response.json().get("certificates")
        self.assertEqual(certificates[0]["certificate_data"], "Data 1")

    def test_valid_post_request_with_incorrect_email_format(self):
        data = {"email": "incorrectformat"}
        response = self.client.post(reverse('get_certificates'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Error fetching certificates", response.json().get("error"))

    def test_valid_post_request_with_missing_email(self):
        response = self.client.post(reverse('get_certificates'), data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Error fetching certificates", response.json().get("error"))
