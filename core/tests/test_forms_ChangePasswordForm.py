# Django
from django.test import TestCase

# App
from core.models import CustomUser
from core.forms import ChangePasswordForm


class ChangePasswordFormTest(TestCase):
    """
    Test ChangePasswordForm
    """

    def setUp(self):
        """
        Pre-set up for testing the form
        """
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="strongPass123",
        )
        self.valid_data = {
            "new_password1": "strongPass456",
            "new_password2": "strongPass456",
        }
        self.invalid_data = {
            "new_password1": "strongPass456",
            "new_password2": "weakPass456",
        }

    def test_form_is_valid(self):
        """
        Test if form is valid with correct data
        """
        form = ChangePasswordForm(user=self.user, data=self.valid_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("strongPass456"))

    def test_form_is_invalid(self):
        """
        Test if form is invalid with incorrect data (mismatched passwords)
        """
        form = ChangePasswordForm(user=self.user, data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("new_password2", form.errors)
