# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.models import MuscleGroup, Exercise


class ExerciseOnUserCreationTest(TestCase):
    """
    Test for signals.py - creating exercises for newly registered users
    """

    def test_default_muscle_groups_creation(self):
        """
        Test to see if newly registered users have all 128 default exercises
        """
        user = CustomUser.objects.create_user(
            username="testuser", email="test@mail.com", password="password123"
        )

        exercises = Exercise.objects.filter(user=user)
        self.assertEqual(exercises.count(), 128)


class ExerciseModelTest(TestCase):
    """
    Tests for Exercise model
    """

    def setUp(self):
        """
        Loading data pre-tests
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", email="mail1@test.com", password="testpass"
        )
        self.musclegroup = MuscleGroup.objects.create(
            user=self.user, name="Test Group"
        )
        self.exercise = Exercise.objects.create(
            user=self.user, musclegroup=self.musclegroup, name="Test Exercise"
        )

    def test_creation(self):
        """
        Test if new exercise is correctly created
        """
        self.assertEqual(self.exercise.name, "Test Exercise")
        self.assertEqual(self.exercise.user, self.user)
        self.assertEqual(self.exercise.musclegroup, self.musclegroup)
        self.assertIsNotNone(self.exercise.created)

    def test_str_representation(self):
        """
        Test model's str method
        """
        expected_str = f"{self.musclegroup} - Exercise: {self.exercise.name}"
        self.assertEqual(str(self.exercise), expected_str)

    def test_fields_max_length_validation(self):
        """
        Test max_length argument for fields
        """
        name = self.exercise.name * 31
        self.assertGreater(len(name), 30)

    def test_delete_user_then_deletes_exercises(self):
        """
        Test if after a user is deleted his exercises will be deleted as well
        """
        self.assertEqual(Exercise.objects.count(), 129)
        self.user.delete()
        self.assertEqual(Exercise.objects.count(), 0)

    def test_delete_musclegroup_then_deletes_exercises(self):
        """
        Test if after a muscle group is deleted his exercises will be deleted
        as well
        """
        self.assertEqual(Exercise.objects.filter(musclegroup=9).count(), 1)
        self.musclegroup.delete()
        self.assertEqual(Exercise.objects.filter(musclegroup=9).count(), 0)
