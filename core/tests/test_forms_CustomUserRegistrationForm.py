# Django
from django.test import TestCase

# App
from core.models import CustomUser
from core.forms import CustomUserRegistrationForm


class CustomUserRegistrationFormTest(TestCase):
    """
    Test CustomUserRegistrationForm
    """

    def setUp(self):
        """
        Pre-set up for testing the form
        """
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@mail.com",
            "password1": "strongPass123",
            "password2": "strongPass123",
        }

        self.invalid_data = {
            "username": "testuser",
            "email": "invalidemail",
            "password1": "password123",
            "password2": "password123",
        }

        self.password_mismatch_data = {
            "username": "testuser",
            "email": "testuser@mail.com",
            "password1": "strongPass123",
            "password2": "strongPass321",
        }

    def test_form_is_valid(self):
        """
        Test if form is valid with correct data
        """
        form = CustomUserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_invalid_email(self):
        """
        Test if form is invalid with an invalid email
        """
        form = CustomUserRegistrationForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_is_invalid_with_password_mismatch(self):
        """
        Test if form is invalid when passwords don't match
        """
        form = CustomUserRegistrationForm(data=self.password_mismatch_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_is_invalid_with_weak_password(self):
        """
        Test if form is invalid when passwords are too weak
        """
        form = CustomUserRegistrationForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_user_creation_on_valid_form(self):
        """
        Test that a user is created when the form is valid
        """
        form = CustomUserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        form.save()
        user = CustomUser.objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@mail.com")
        self.assertTrue(user.check_password("strongPass123"))

    def test_user_not_created_on_invalid_form(self):
        """
        Test that no user is created if the form is invalid
        """
        form = CustomUserRegistrationForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(username="testuser")
