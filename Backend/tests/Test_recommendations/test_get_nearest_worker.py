from django.test import TestCase, RequestFactory
from django.urls import reverse
from HandymanHive.models import Service, WorkerDetails, CustomWorker
from HandymanHive.routes.recommendation import get_nearest_workers
import json

class GetNearestWorkersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Create test data
        self.service = Service.objects.create(name="Test Service")
        self.worker = CustomWorker.objects.create(email="test@example.com", first_name="John", last_name="Doe",age=30)
        self.worker_details = WorkerDetails.objects.create(
            email=self.worker,
            isAvailable=True,
            min_price=10,
            max_price=20,
            liveLatitude=10, 
            liveLongitude=20
        )
        self.worker_details.services_offered.add(self.service)

    def test_get_nearest_workers(self):
        request = self.factory.post(reverse('get_nearest_workers'), json.dumps({"service": "Test Service", "coords": [0, 0]}), content_type='application/json')
        response = get_nearest_workers(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['workers']), 1)

    def test_service_does_not_exist(self):
        request = self.factory.post(reverse('get_nearest_workers'), json.dumps({"service": "Nonexistent Service", "coords": [0, 0]}), content_type='application/json')
        response = get_nearest_workers(request)

        self.assertEqual(response.status_code, 500)

    def test_invalid_request_method(self):
        request = self.factory.get(reverse('get_nearest_workers'))
        response = get_nearest_workers(request)

        self.assertEqual(response.status_code, 400)
