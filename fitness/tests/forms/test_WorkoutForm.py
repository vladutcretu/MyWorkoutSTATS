# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.forms import WorkoutForm


class WorkoutFormTest(TestCase):
    """
    Test WorkoutForm
    """

    def setUp(self):
        """
        Pre-set up for testing the form
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@mail.com", password="password123"
        )
        self.valid_data = {
            "name": "Test Workout",
            "bodyweight": "100",
            "note": "abc",
            "public": "yes",
        }
        self.invalid_data = {
            "name": "Test Workout",
            "bodyweight": "abc",
            "note": "",
            "public": "okey",
        }

    def test_form_is_valid(self):
        """
        Test if form is valid with correct data
        """
        form = WorkoutForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        """
        Test if form is valid with incorrect data
        """
        form = WorkoutForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
