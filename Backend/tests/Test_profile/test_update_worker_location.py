import json
from django.test import TestCase
from django.urls import reverse
from HandymanHive.models import WorkerDetails
from HandymanHive.routes.profile import update_worker_location
from django.http import JsonResponse

class TestUpdateWorkerLocation(TestCase):
    def setUp(self):
        # Create WorkerDetails instances for testing
        self.worker1 = WorkerDetails.objects.create(
            email='worker1@example.com',
            liveLatitude=0.0,
            liveLongitude=0.0
        )
        self.worker2 = WorkerDetails.objects.create(
            email='worker2@example.com',
            liveLatitude=0.0,
            liveLongitude=0.0
        )

    def test_update_worker_location_success(self):
        # Test for successful worker location update
        request_body = {
            "email": "worker1@example.com",
            "liveLatitude": 40.7128,
            "liveLongitude": -74.0060
        }
        response = self.client.post(reverse("update_worker_location"), json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Worker location updated successfully"})
        # Assert that the worker's location has been updated in the database
        updated_worker = WorkerDetails.objects.get(email='worker1@example.com')
        self.assertEqual(updated_worker.liveLatitude, 40.7128)
        self.assertEqual(updated_worker.liveLongitude, -74.0060)

    def test_update_worker_location_missing_email(self):
        # Test for missing email key in request
        request_body = {
            "liveLatitude": 40.7128,
            "liveLongitude": -74.0060
        }
        response = self.client.post(reverse("update_worker_location"), json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Worker not found"})

    def test_update_worker_location_missing_coordinates(self):
        # Test for missing latitude and/or longitude keys in request
        request_body = {
            "email": "worker1@example.com",
        }
        response = self.client.post(reverse("update_worker_location"), json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Error updating worker location"})

    def test_update_worker_location_non_existing_worker(self):
        # Test for non-existing worker
        request_body = {
            "email": "nonexisting@example.com",
            "liveLatitude": 40.7128,
            "liveLongitude": -74.0060
        }
        response = self.client.post(reverse("update_worker_location"), json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Worker not found"})

    def test_update_worker_location_non_numeric_coordinates(self):
        # Test for non-numeric latitude or longitude
        request_body = {
            "email": "worker1@example.com",
            "liveLatitude": "invalid",
            "liveLongitude": -74.0060
        }
        response = self.client.post(reverse("update_worker_location"), json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Error updating worker location"})


    def test_update_worker_location_invalid_request_method(self):
        # Test for invalid request method
        response = self.client.get(reverse("update_worker_location"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request method"})

    def test_update_worker_location_successful_update_existing_coordinates(self):
        # Test for successful update with existing coordinates
        request_body = {
            "email": "worker1@example.com",
            "liveLatitude": 0.0,
            "liveLongitude": 0.0
        }
        response = self.client.post(reverse("update_worker_location"), json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Worker location updated successfully"})
        # Assert that the worker's location remains unchanged in the database
        updated_worker = WorkerDetails.objects.get(email='worker1@example.com')
        self.assertEqual(updated_worker.liveLatitude, 0.0)
        self.assertEqual(updated_worker.liveLongitude, 0.0)

    def test_update_worker_location_missing_email_and_coordinates(self):
        # Test for missing email and coordinates in request
        request_body = {}
        response = self.client.post(reverse("update_worker_location"), json.dumps(request_body), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Worker not found"})
