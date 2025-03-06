# Django
from django.test import TestCase

# App
from core.models import CustomUser
from core.forms import AccountRecoveryForm


class AccountRecoveryFormTest(TestCase):
    """
    Test AccountRecoveryForm
    """

    def setUp(self):
        """Pre-set up for testing the form"""
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="strongPass123",
        )

        self.valid_data = {
            "email": "testuser@mail.com",
        }

        self.invalid_data = {
            "email": "invalidemail",
        }

    def test_form_is_valid(self):
        """Test if form is valid with correct data"""
        form = AccountRecoveryForm(data=self.valid_data)
        # if not form.is_valid():
        #     print(form.errors)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = AccountRecoveryForm(data=self.invalid_data)
        # if not form.is_valid():
        #     print(form.errors)
        self.assertFalse(form.is_valid())
