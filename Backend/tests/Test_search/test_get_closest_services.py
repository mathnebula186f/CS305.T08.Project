from django.test import TestCase, Client
from HandymanHive.models import CustomUser, CustomWorker, Service
import json
from unittest.mock import patch
from django.urls import reverse


class GetClosestServicesTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        
    def test_successful_query_processing(self):
        # Create a CustomUser for testing
        user_email = "test@example.com"
        CustomUser.objects.create(email=user_email,age=20)

        # Send a POST request with valid data
        data = {"query": "leaking sink", "email": user_email}
        url=reverse("get_closest_services")
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('services', response.json())
        self.assertIn('workers', response.json())

    def test_query_processing_with_invalid_email(self):
        # Send a POST request with an invalid email
        data = {"query": "leaking sink", "email": "invalid_email@example.com"}
        url=reverse("get_closest_services")
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())

    def test_query_processing_with_missing_data(self):
        # Send a POST request with missing data
        data = {"query": "leaking sink"}
        url=reverse("get_closest_services")
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())

    def test_query_processing_with_no_workers_found(self):
        # Create a CustomUser for testing
        user_email = "test@example.com"
        CustomUser.objects.create(email=user_email,age=20)

        # Send a POST request with a query that doesn't match any workers
        data = {"query": "non_existent_query", "email": user_email}
        url = reverse("get_closest_services")
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_invalid_request_method(self):
        # Send a GET request instead of a POST request
        response = self.client.get(reverse("get_closest_services"))
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

