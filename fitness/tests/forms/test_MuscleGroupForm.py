# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.forms import MuscleGroupForm


class MuscleGroupFormTest(TestCase):
    """
    MuscleGroupForm
    """

    def setUp(self):
        """
        Pre-set up for testing the form
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@mail.com", password="password123"
        )
        self.valid_data = {"name": "Test Group"}
        self.invalid_data = {"name": ""}

    def test_form_is_valid(self):
        """
        Test if form is valid with correct data
        """
        form = MuscleGroupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        """
        Test if form is valid with incorrect data
        """
        form = MuscleGroupForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
