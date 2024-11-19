# Django
from django.test import TestCase
from django.db import IntegrityError

# App
from core.models import CustomUser

class CustomUserModelTest(TestCase):
    """Tests for CustomUser model"""
    def setUp(self):
        """Load data pre-tests"""
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testmail@testuser.com",
            password="password123",
            profile_picture = "default.jpg",
            first_name="Test",
            last_name="User",
            age=18,
            city="Bucharest",
            bio="This is a test bio",
            instagram_url="https://instagram.com/testuser"
        )
    
    def test_fields_completed(self):
        """Test if all fields can be completed."""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testmail@testuser.com")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.profile_picture, "default.jpg")
        self.assertEqual(self.user.age, 18)
        self.assertEqual(self.user.city, "Bucharest")
        self.assertEqual(self.user.bio, "This is a test bio")
        self.assertEqual(self.user.instagram_url, "https://instagram.com/testuser")

    def test_str_representation(self):
        """Test model's str method"""
        self.assertEqual(str(self.user), self.user.username)

    def test_fields_blank_null(self):
        """Test if fields constraints are working (blank and null)"""
        user = CustomUser.objects.create_user(
            username="test_user",
            email="test_mail@testuser.com",
            password="password123",
        )
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.password)
        self.assertIsNone(user.first_name)
        self.assertIsNone(user.last_name)
        self.assertIsNone(user.age)
        self.assertIsNone(user.city)
        self.assertIsNone(user.bio)
        self.assertIsNone(user.instagram_url)
    
    def test_fields_max_length_validation(self):
        """Test max_length argument for fields"""
        first_name = self.user.first_name * 31
        last_name = self.user.last_name * 31
        city = self.user.city * 31
        bio = self.user.bio * 301
        instagram_url = self.user.instagram_url * 101
        self.assertGreater(len(first_name), 30)
        self.assertGreater(len(last_name), 30)
        self.assertGreater(len(city), 30)
        self.assertGreater(len(bio), 300)
        self.assertGreater(len(instagram_url), 100)

    def test_name_is_unique(self):
        """Test if name field is unique"""
        with self.assertRaises(IntegrityError): 
            CustomUser.objects.create_user(
                username="testuser",
                email="testmail@testuser.com",
                password="password123"
            )

    def test_email_is_unique(self):
        """Test if email field is unique"""
        with self.assertRaises(IntegrityError): 
            CustomUser.objects.create_user(
                username="test_user",
                email="testmail@testuser.com",
                password="password123"
            )