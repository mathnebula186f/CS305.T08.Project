import json
import base64
from django.test import TestCase
from django.urls import reverse
from HandymanHive.models import Certification  # Assuming your model is named Certification
from django.http import JsonResponse
import unittest.mock


class UploadCertificateTestCase(TestCase):
    def test_upload_certificate_success(self):
        # Prepare valid data for the POST request
        data = {
            'email': 'example@example.com',
            'certificate_name': 'Certificate of Achievement',
            'certificate': base64.b64encode(b'This is a certificate').decode('utf-8')
        }

        # Make a POST request to the view
        response = self.client.post(reverse('upload_certificate'), json.dumps(data), content_type='application/json')

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Certificate uploaded successfully'})
        self.assertTrue(Certification.objects.filter(certificate_name='Certificate of Achievement').exists())

    def test_upload_certificate_invalid_request_method(self):
        # Make a GET request to the view
        response = self.client.get(reverse('upload_certificate'))

        # Check if the response is as expected
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid request method'})

    def test_upload_certificate_invalid_data(self):
        # Prepare invalid data for the POST request (missing 'email' field)
        data = {
            'certificate_name': 'Certificate of Achievement',
            'certificate': base64.b64encode(b'This is a certificate').decode('utf-8')
        }

        # Make a POST request to the view
        response = self.client.post(reverse('upload_certificate'), json.dumps(data), content_type='application/json')

        # Check if the response is as expected
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'error': 'Error uploading certificate'})

    def test_upload_certificate_exception(self):
        # Mock an exception during certificate upload
        with unittest.mock.patch('HandymanHive.routes.profile.Certification.objects.create') as mock_create:
            mock_create.side_effect = Exception("Something went wrong")

            # Prepare valid data for the POST request
            data = {
                'email': 'example@example.com',
                'certificate_name': 'Certificate of Achievement',
                'certificate': base64.b64encode(b'This is a certificate').decode('utf-8')
            }

            # Make a POST request to the view
            response = self.client.post(reverse('upload_certificate'), json.dumps(data), content_type='application/json')

            # Check if the response is as expected
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {'error': 'Error uploading certificate'})
            mock_create.assert_called_once()

    def test_upload_certificate_empty_data(self):
        # Prepare empty data for the POST request
        data = {}

        # Make a POST request to the view
        response = self.client.post(reverse('upload_certificate'), json.dumps(data), content_type='application/json')

        # Check if the response is as expected
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'error': 'Error uploading certificate'})
