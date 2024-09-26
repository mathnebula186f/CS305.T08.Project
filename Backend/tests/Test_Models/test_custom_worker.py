from django.test import TestCase
from HandymanHive.models import CustomWorker
from django.core.exceptions import ValidationError
from datetime import timedelta,datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.utils import DataError, IntegrityError

class CustomWorkerTestCase(TestCase):
    def setUp(self):
        self.worker_data = {
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'gender': 'Male',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
            'otp': '123456',
            'otp_valid_till': timezone.now(),
            'notification_token': 'abc123'
        }
        
    def test_create_custom_worker(self):
        worker = CustomWorker.objects.create(**self.worker_data)
        self.assertEqual(worker.email, 'test@example.com')
        self.assertEqual(worker.phone_number, '1234567890')
        self.assertEqual(worker.first_name, 'John')
        self.assertEqual(worker.last_name, 'Doe')
        self.assertEqual(worker.age, 30)
        self.assertEqual(worker.gender, 'Male')
        self.assertEqual(worker.address, '123 Test St')
        self.assertEqual(worker.city, 'Test City')
        self.assertEqual(worker.state, 'Test State')
        self.assertEqual(worker.zip_code, '12345')
        self.assertEqual(worker.otp, '123456')
        self.assertEqual(worker.notification_token, 'abc123')

    def test_unique_email_and_phone_number(self):
        CustomWorker.objects.create(**self.worker_data)
        duplicate_data = self.worker_data.copy()
        duplicate_data['phone_number'] = '0987654321'
        with self.assertRaises(IntegrityError):
            CustomWorker.objects.create(**duplicate_data)

    def test_otp_valid_till_boundary(self):
        expired_worker_data = self.worker_data.copy()
        expired_worker_data['otp_valid_till'] = timezone.now() - timedelta(minutes=20)
        with self.assertRaises(ValidationError):
            CustomWorker.objects.create(**expired_worker_data)

    def test_notification_token_optional(self):
        # Test if notification_token is optional
        del self.worker_data['notification_token']
        worker = CustomWorker.objects.create(**self.worker_data)
        self.assertIsNone(worker.notification_token)

    def test_email_max_length(self):
        self.worker_data['email'] = 'a' * 256
        with self.assertRaises(DataError):
            CustomWorker.objects.create(**self.worker_data)

    def test_phone_number_max_length(self):
        self.worker_data['phone_number'] = '1' * 16
        with self.assertRaises(DataError):
            CustomWorker.objects.create(**self.worker_data)

    def test_notification_token_max_length(self):
        self.worker_data['notification_token'] = 'a' * 256
        with self.assertRaises(DataError):
            CustomWorker.objects.create(**self.worker_data)

    def test_missing_required_fields(self):
        incomplete_data = self.worker_data.copy()
        del incomplete_data['email']
        with self.assertRaises(ValidationError):
            CustomWorker.objects.create(**incomplete_data)  

    def test_invalid_email_format(self):
        self.worker_data['email'] = 'invalid_email'
        with self.assertRaises(ValidationError):
            CustomWorker.objects.create(**self.worker_data)  

    def test_age_less_than_zero(self):
        self.worker_data['age'] = -5
        with self.assertRaises(ValidationError):
            CustomWorker.objects.create(**self.worker_data)


class CustomWorkerIntegrationTestCase(TestCase):
    
    def setUp(self):
        self.worker_data = {
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'gender': 'Male',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
        }
        
    def test_create_and_retrieve_worker(self):
        CustomWorker.objects.create(**self.worker_data)
        try:
            worker = CustomWorker.objects.get(email='test@example.com')
            self.assertEqual(worker.first_name, 'John')
            self.assertEqual(worker.last_name, 'Doe')
        except ObjectDoesNotExist:
            self.fail("Failed to retrieve the created CustomWorker object")
    
    def test_update_worker_details(self):
        worker = CustomWorker.objects.create(**self.worker_data)
        worker.first_name = 'Jane'
        worker.save()
        updated_worker = CustomWorker.objects.get(email='test@example.com')
        self.assertEqual(updated_worker.first_name, 'Jane')

    def test_delete_worker(self):
        worker = CustomWorker.objects.create(**self.worker_data)
        worker.delete()
        with self.assertRaises(ObjectDoesNotExist):
            CustomWorker.objects.get(email='test@example.com')

class CustomWorkerPerformanceTestCase(TestCase):

    def test_create_large_number_of_workers(self):
        start_time = datetime.now()
        for i in range(1000):
            CustomWorker.objects.create(
                email=f'test{i}@example.com',
                phone_number=f'12345678{i}',
                first_name='John',
                last_name='Doe',
                age=30,
                gender='Male',
                address='123 Test St',
                city='Test City',
                state='Test State',
                zip_code='12345',
            )
        end_time = datetime.now()
        duration = end_time - start_time
        self.assertLess(duration.total_seconds(), 10, "Creation of 1000 workers took more than 10 seconds")