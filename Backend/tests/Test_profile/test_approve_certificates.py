import json
from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import Certification
from unittest.mock import patch
import base64

class ApproveCertificateTestCase(TestCase):
    def setUp(self):
        # Create a sample certification instance for testing
        certificate_data = "Data 1"
        encoded_certificate_data = base64.b64encode(certificate_data.encode())
        self.certification = Certification.objects.create(
            certificate_name="Certificate 1",
            issuing_authority="Authority 1",
            certificate_data=encoded_certificate_data,
            worker_email="test@example.com",
            status="Pending"
        )
        self.client = Client()

    def test_approve_certificate_success(self):
        url = reverse('approve_certificate')
        data = {
            "worker_email": "test@example.com",
            "certificate_name": "Certificate 1"
        }
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Certification.objects.get(pk=self.certification.pk).status, "Approved")
        self.assertEqual(response.json(), {"message": "Certificate approved successfully"})

    def test_approve_certificate_not_found(self):
        url = reverse('approve_certificate')
        data = {
            "worker_email": "test@example.com",
            "certificate_name": "Non-existent Certificate"
        }
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Certificate not found"})

    def test_approve_certificate_invalid_method(self):
        url = reverse('approve_certificate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request method"})

    def test_approve_certificate_exception(self):
        url = reverse('approve_certificate')
        data = {
            "worker_email": "test@example.com",
            "certificate_name": "Certificate 1"
        }
        # Simulate an exception during certificate approval
        with patch('HandymanHive.models.Certification.objects.get') as mock_get:
            mock_get.side_effect = Exception("Simulated error")
            response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Error approving certificate"})
