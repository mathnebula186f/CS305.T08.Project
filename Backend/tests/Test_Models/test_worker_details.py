from django.test import TestCase
from HandymanHive.models import WorkerDetails
from django.core.exceptions import ValidationError
from django.db.utils import DataError

class WorkerDetailsTestCase(TestCase):


    def setUp(self):
        self.worker_data = {
            'email': 'test@example.com',
            'skill_level': 5,
            'isAvailable': True,
            'liveLatitude': 0.0,
            'liveLongitude': 0.0,
            'preferred_location': 'Test location',
            'work_history': 'Test work history',
            'years_of_experience': 3,
            'customer_reviews': 'Test customer reviews',
            'overall_rating': 4.5,
            'training_programs_completed': 'Test training programs completed',
            'min_price': 10.0,
            'max_price': 20.0,
        }
        self.services= ["Plumbing", "Electrical"]

    def test_unique_email(self):
        worker1 = WorkerDetails.objects.create(**self.worker_data)
        with self.assertRaises(Exception):
            WorkerDetails.objects.create(email='test@example.com')

    def test_min_price_decimal_places(self):
        worker = WorkerDetails.objects.create(**self.worker_data)
        decimal_places = worker._meta.get_field('min_price').decimal_places
        self.assertEqual(decimal_places, 2)

    def test_skill_level_range(self):
        worker = WorkerDetails.objects.create(**self.worker_data)
        self.assertTrue(0 <= worker.skill_level <= 10)
    
    def test_min_price_less_than_max_price(self):
        worker = WorkerDetails.objects.create(**self.worker_data)
        self.assertLessEqual(worker.min_price, worker.max_price)

    def test_preferred_location_blank(self):
        self.worker_data['preferred_location'] = ''
        worker = WorkerDetails.objects.create(**self.worker_data)
        self.assertEqual(worker.preferred_location, '')

    def test_customer_reviews_blank(self):
        self.worker_data['customer_reviews'] = ''
        worker = WorkerDetails.objects.create(**self.worker_data)
        self.assertEqual(worker.customer_reviews, '')

    def test_email_max_length(self):
        self.worker_data['email'] = 'a' * 256
        with self.assertRaises(DataError):
            WorkerDetails.objects.create(**self.worker_data)

    def test_skill_level_range(self):
        self.worker_data['skill_level'] = 15
        with self.assertRaises(ValidationError):
            WorkerDetails.objects.create(**self.worker_data)

    def test_overall_rating_range(self):
        self.worker_data['overall_rating'] = 11.0
        with self.assertRaises(ValidationError):
            WorkerDetails.objects.create(**self.worker_data)

    def test_training_programs_blank(self):
        self.worker_data['training_programs_completed'] = ''
        WorkerDetails.objects.create(**self.worker_data)

    def test_work_history_blank(self):
        self.worker_data['work_history'] = ''
        WorkerDetails.objects.create(**self.worker_data)

