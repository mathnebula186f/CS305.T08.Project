from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from HandymanHive.routes import get_services
from HandymanHive.models import WorkerDetails, Service
import json

class GetServicesViewTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.worker = WorkerDetails.objects.create(email="test@example.com")
        self.service1 = Service.objects.create(name="Service 1")
        self.service2 = Service.objects.create(name="Service 2")
        self.worker.services_offered.add(self.service1, self.service2)

    def test_get_services_post(self):
        # Prepare a POST request
        data = {
            "email": "test@example.com"
        }
        request = RequestFactory().post('/get_services/', json.dumps(data), content_type='application/json')

        # Call the view function
        response = get_services(request)

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        expected_response = [{"name": "Service 1"}, {"name": "Service 2"}]
        self.assertEqual(json.loads(response.content), expected_response)

    def test_get_services_get(self):
        # Prepare a GET request
        request = RequestFactory().get('/get_services/')

        # Call the view function
        response = get_services(request)

        # Check if the response is as expected
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"error": "Invalid request method"})
