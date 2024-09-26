import json
import base64
from io import BytesIO
from PIL import Image
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import CustomUser, CustomWorker

class UploadProfilePicTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('upload_profile_pic')  # replace with your actual url name
        self.user = CustomUser.objects.create(email='user@test.com',age=30)
        self.worker = CustomWorker.objects.create(email='worker@test.com', age=29)

    def generate_random_image(self):
        # Generate a random image
        img = Image.new('RGB', (60, 30), color = (73, 109, 137))
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        return base64.b64encode(img_byte_arr).decode('utf-8')

    def test_upload_profile_pic_post_user(self):
        img_data = self.generate_random_image()
        data = {
            "email": self.user.email,
            "isWorker": "False",
            "image": img_data
        }
        with patch('cloudinary.uploader.upload', return_value={'secure_url': 'https://test.com/image.jpg'}):
            response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['url'], 'https://test.com/image.jpg')

    def test_upload_profile_pic_post_worker(self):
        img_data = self.generate_random_image()
        data = {
            "email": self.worker.email,
            "isWorker": "True",
            "image": img_data
        }
        with patch('cloudinary.uploader.upload', return_value={'secure_url': 'https://test.com/image.jpg'}):
            response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['url'], 'https://test.com/image.jpg')

    def test_upload_profile_pic_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_upload_profile_pic_user_not_found(self):
        data = {
            "email": 'nonexistent@test.com',
            "isWorker": "False",
            "image": 'test'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_upload_profile_pic_exception(self):
        img_data = self.generate_random_image()
        data = {
            "email": self.user.email,
            "isWorker": "False",
            "image": img_data
        }
        with patch('cloudinary.uploader.upload', side_effect=Exception('Cloudinary error')):
            response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
