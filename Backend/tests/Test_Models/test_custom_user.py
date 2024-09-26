from django.test import TestCase
from HandymanHive.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import timedelta,datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.utils import DataError, IntegrityError

class CustomUserTest(TestCase):

    def setUp(self):
        self.user_data = {
            "email":"valid@email.com",
            "phone_number":"1234567890",
            "first_name":"John",
            "last_name":"Doe",
            "age":30,
            "gender":"Male",
            "address":"123 Main St",
            "city":"Anytown",
            "state":"CA",
            "zip_code":"12345"
        }
    
    def test_create_valid_user(self):
        user = CustomUser.objects.create(
            email="valid@email.com",
            phone_number="1234567890",
            first_name="John",
            last_name="Doe",
            age=30,
            gender="Male",
            address="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="12345",
        )
        self.assertEqual(user.email, "valid@email.com")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.age, 30)
        self.assertEqual(user.gender, "Male")
        self.assertEqual(user.address, "123 Main St")
        self.assertEqual(user.city, "Anytown")
        self.assertEqual(user.state, "CA")
        self.assertEqual(user.zip_code, "12345")
        self.assertEqual(user.last_five_queries, [])
    
    # TESTING EMAILS
    def test_create_user_with_invalid_email(self):
        user_data = self.user_data.copy()

        # Missing "@" symbol
        with self.assertRaises(ValidationError):
            user_data["email"] = "johndoeexample.com"
            CustomUser.objects.create(**user_data)

        # Missing domain name
        user_data = self.user_data.copy()
        with self.assertRaises(ValidationError):
            user_data["email"] = "johndoe@"
            CustomUser.objects.create(**user_data)

        # Invalid domain name (no top-level domain)
        user_data = self.user_data.copy()
        with self.assertRaises(ValidationError):
            user_data["email"] = "johndoe@invaliddomain"
            CustomUser.objects.create(**user_data)

        # Empty email
        user_data = self.user_data.copy()
        with self.assertRaises(ValidationError):
            user_data["email"] = ""
            CustomUser.objects.create(**user_data)

    def test_create_user_with_duplicate_email(self):
        user_data = self.user_data.copy()

        # Create user1 with the email to be duplicated
        user_data["email"] = "duplicate@email.com"
        user1 = CustomUser.objects.create(**user_data)

        # Create user2 with the same email as user1 (duplicate)
        user2_data = user_data.copy()
        user2_data["email"] = user1.email  # Set user2's email to match user1's
        with self.assertRaises(IntegrityError):  # Assuming unique email constraint
            CustomUser.objects.create(**user2_data)

    # TESTING PHONE NO.
    def test_create_user_with_invalid_phone_number_non_numeric(self):
        user_data = self.user_data.copy()
        user_data["phone_number"] = "1234abc567"
        # Non-numeric characters
        with self.assertRaises(ValidationError):
            CustomUser.objects.create(**user_data)
    
    
    def test_create_user_with_invalid_phone_number_too_long(self):
        user_data = self.user_data.copy()
        user_data["phone_number"] = "1234567890123454545"
        # Too long
        with self.assertRaises(DataError):
            CustomUser.objects.create(**user_data)
            
    def test_create_user_with_invalid_phone_number_empty(self):
        user_data = self.user_data.copy()
        user_data["phone_number"] = ""
        # Non-numeric characters
        with self.assertRaises(ValidationError):
            CustomUser.objects.create(**user_data)


    def test_create_user_with_duplicate_phone_number(self):
        user_data = self.user_data.copy()
        
        user_data["phone_number"] = "1234567890"
        user1 = CustomUser.objects.create(**user_data)
        
        user2_data = user_data.copy()
        user2_data["phone_number"] = user1.phone_number
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(**user2_data)

    
    # TESTING NAME
    def test_create_user_with_empty_name(self):
        user_data = self.user_data.copy()
        user_data["first_name"] = ""
        with self.assertRaises(ValidationError):
            CustomUser.objects.create(**user_data)

    def test_create_user_with_name_exceeding_length(self):
        long_name = "A" * 31  # Name exceeding maximum length (assuming 30)
        user_data = self.user_data.copy()
        user_data["first_name"] = long_name
        with self.assertRaises(DataError):
            CustomUser.objects.create(**user_data)

    # TESTING AGE
    def test_create_user_with_invalid_age_negative(self):
        user_data = self.user_data.copy()
        user_data["age"] = -10
        with self.assertRaises(ValidationError):
            CustomUser.objects.create(**user_data)

    # TESTING GENDER
    def test_create_user_with_invalid_gender(self):
        user_data = self.user_data.copy()
        user_data["gender"] = "InvalidGender"
        with self.assertRaises(DataError):
            CustomUser.objects.create(**user_data)

    
    # TESTING EMPTY FIELDS
    def test_create_user_with_empty_optional_fields(self):
        user = self.user_data.copy()
        user["address"] = ""
        user['city'] = ''
        user['state'] = ''
        user['zip_code'] = ''

        # Assuming address, city, state, and zip_code are optional:
        self.assertEqual(user["address"], "")
        self.assertEqual(user["city"], '')
        self.assertEqual(user["state"], '')
        self.assertEqual(user["zip_code"], '')
        
        
    # TESTING OTP
    def test_create_user_with_valid_otp_and_valid_till(self):
        future_time = timezone.now() + timedelta(days=1)
        user_data = self.user_data.copy()
        user_data['otp'] = '123456'
        user_data['otp_valid_till'] = future_time
        user = CustomUser.objects.create(
            **user_data
        )
        self.assertEqual(user.otp, '123456')
        self.assertGreater(user.otp_valid_till, timezone.now())

    def test_create_user_with_empty_otp_and_null_valid_till(self):
        user_data = self.user_data.copy()
        user = CustomUser.objects.create(
            **user_data
        )
        
        self.assertEqual(user.otp, None)
        self.assertEqual(user.otp_valid_till, None)

    def test_create_user_with_invalid_otp_length(self):
        user_data = self.user_data.copy()
        user_data['otp'] = '12345678'
        # Too long
        with self.assertRaises(DataError):
            CustomUser.objects.create(**user_data)
    
    # TESTING add_query FUNCTION
    def test_add_query_with_empty_query(self):
        # Adjust this test based on whether empty queries are allowed
        user_data = self.user_data.copy()
        user = CustomUser.objects.create(
            **user_data
        )
        with self.assertRaises(ValidationError):
            user.add_query("")

    # TESTING get_last_five_queries FUNCTION
    def test_add_more_than_five_queries(self):
        user_data = self.user_data.copy()
        user = CustomUser.objects.create(
            **user_data
        )
        
        for i in range(6):
            user.add_query(f"Query {i+1}")
        self.assertEqual(len(user.last_five_queries), 5)
        self.assertEqual(user.last_five_queries[0], "Query 2")  # Last added should be first

    def test_get_last_five_queries(self):
        user_data = self.user_data.copy()
        user = CustomUser.objects.create(
            **user_data
        )
        user.add_query("Query 1")
        user.add_query("Query 2")
        user.add_query("Query 3")

        # Test get_last_five_queries after adding some queries
        self.assertEqual(user.get_last_five_queries(), ["Query 1", "Query 2", "Query 3"])

        # Test get_last_five_queries with an empty list
        user.last_five_queries = []
        self.assertEqual(user.get_last_five_queries(), [])
