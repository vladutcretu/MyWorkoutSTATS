# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.models import MuscleGroup
from fitness.forms import ExerciseForm


class ExerciseFormTest(TestCase):
    """
    Test ExerciseForm
    """

    def setUp(self):
        """
        Pre-set up for testing the form
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@mail.com", password="password123"
        )
        self.musclegroup = MuscleGroup.objects.create(
            user=self.user, name="Test Group"
        )
        self.valid_data = {
            "name": "Test Exercise",
            "musclegroup": self.musclegroup.id,
        }
        self.invalid_data = {"name": "", "musclegroup": ""}

    def test_form_is_valid(self):
        """
        Test if form is valid with correct data
        """
        form = ExerciseForm(user=self.user, data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        """
        Test if form is valid with incorrect data
        """
        form = ExerciseForm(user=self.user, data=self.invalid_data)
        self.assertFalse(form.is_valid())
