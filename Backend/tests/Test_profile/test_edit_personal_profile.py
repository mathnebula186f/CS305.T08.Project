import json
from django.test import TestCase
from django.urls import reverse
from HandymanHive.models import CustomWorker, CustomUser
from HandymanHive.routes.profile import edit_personal_profile

class TestEditPersonalProfile(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.worker_data = {
            "email": "worker@example.com",
            "phone_number": "1234567890",
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "gender": "Male",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001"
        }
        self.user_data = {
            "email": "user@example.com",
            "phone_number": "9876543210",
            "first_name": "Jane",
            "last_name": "Doe",
            "age": 25,
            "gender": "Female",
            "address": "456 Elm St",
            "city": "Los Angeles",
            "state": "CA",
            "zip_code": "90001"
        }

        # Create sample worker and user
        self.worker = CustomWorker.objects.create(**self.worker_data)
        self.user = CustomUser.objects.create(**self.user_data)

    def test_edit_personal_profile_success(self):
        # Test for successful profile update
        updated_data = {
            "email": "worker@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "age": 35,
            "gender": "Other",
            "address": "789 Oak St",
            "city": "Chicago",
            "state": "IL",
            "zip_code": "60601",
            "phone_number": "5555555555",
            "isWorker": "True"
        }
        response = self.client.post(reverse("edit_personal_profile"), json.dumps(updated_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomWorker.objects.get(email="worker@example.com").first_name, "Updated")

    def test_edit_personal_profile_invalid_email(self):
        # Test for invalid email
        invalid_email_data = {
            "email": "invalidexample.com",
            "first_name": "Updated",
            "last_name": "Name",
            "age": 35,
            "gender": "Other",
            "address": "789 Oak St",
            "city": "Chicago",
            "state": "IL",
            "zip_code": "60601",
            "phone_number": "5555555555",
            "isWorker": "True"
        }
        response = self.client.post(reverse("edit_personal_profile"), json.dumps(invalid_email_data), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_edit_personal_profile_exception(self):
        # Test for internal server error
        invalid_data = {
            "email": "worker@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "age": "Invalid",  # Age should be an integer, this will cause an exception
            "gender": "Other",
            "address": "789 Oak St",
            "city": "Chicago",
            "state": "IL",
            "zip_code": "60601",
            "phone_number": "5555555555",
            "isWorker": "True",
        }
        response = self.client.post(reverse("edit_personal_profile"), json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_edit_personal_profile_worker_not_found(self):
        # Test for worker not found
        data = {
            "email": "unknown_worker@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "gender": "Male",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "phone_number": "1234567890",
            "isWorker": "True",
        }
        response = self.client.post(reverse("edit_personal_profile"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_edit_personal_profile_user_not_found(self):
        # Test for user not found
        data = {
            "email": "unknown_user@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "age": 25,
            "gender": "Female",
            "address": "456 Elm St",
            "city": "Los Angeles",
            "state": "CA",
            "zip_code": "90001",
            "phone_number": "9876543210",
            "isWorker": "False",
        }
        response = self.client.post(reverse("edit_personal_profile"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 500)
