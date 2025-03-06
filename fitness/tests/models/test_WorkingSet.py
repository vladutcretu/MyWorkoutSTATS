# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.models import (
    MuscleGroup,
    Exercise,
    Workout,
    WorkingSet,
    WorkoutExercise,
)


class WorkingSetModelTest(TestCase):
    """
    Tests for WorkingSet model
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
        self.workout = Workout.objects.create(
            user=self.user, name="Test Workout", created="2024-12-01"
        )
        self.workout_exercise = WorkoutExercise.objects.create(
            workout=self.workout, exercise=self.exercise, order=1
        )
        self.workingset = WorkingSet.objects.create(
            user=self.user,
            workout=self.workout,
            exercise=self.exercise,
            created="2024-12-01",
        )

    def test_creation(self):
        """
        Test if new exercise is correctly created
        """
        self.assertEqual(self.workingset.user, self.user)
        self.assertEqual(self.workingset.workout, self.workout)
        self.assertEqual(self.workingset.exercise, self.exercise)
        self.assertEqual(self.workingset.type, "working")
        self.assertIsNone(self.workingset.weight)
        self.assertIsNone(self.workingset.repetitions)
        self.assertIsNone(self.workingset.distance)
        self.assertIsNone(self.workingset.time)
        self.assertIsNotNone(self.workingset.updated)
        self.assertIsNotNone(self.workingset.created)

    def test_str_representation(self):
        """
        Test model's str method
        """
        expected_str = (
            f"{self.exercise} - Set "
            f"{self.workingset.weight} weight, "
            f"{self.workingset.repetitions} reps | "
            f"{self.workingset.distance} meters, "
            f"{self.workingset.time} minutes "
        )
        self.assertEqual(str(self.workingset), expected_str)

    def test_delete_user_then_deletes_workingsets(self):
        """
        Test if after a user is deleted his working sets will be deleted
        as well
        """
        self.assertEqual(WorkingSet.objects.count(), 1)
        self.user.delete()
        self.assertEqual(WorkingSet.objects.count(), 0)

    def test_delete_workout_then_deletes_workingsets(self):
        """
        Test if after a workout is deleted his working sets will be deleted
        as well
        """
        self.assertEqual(WorkingSet.objects.count(), 1)
        self.workout.delete()
        self.assertEqual(WorkingSet.objects.count(), 0)

    def test_delete_musclegroup_then_deletes_workingsets(self):
        """
        Test if after a musclegroup is deleted his working sets will be deleted
        as well
        """
        self.assertEqual(WorkingSet.objects.count(), 1)
        self.musclegroup.delete()
        self.assertEqual(WorkingSet.objects.count(), 0)

    def test_delete_exercise_then_deletes_workingsets(self):
        """
        Test if after a exercise is deleted his working sets will be deleted
        as well
        """
        self.assertEqual(WorkingSet.objects.count(), 1)
        self.exercise.delete()
        self.assertEqual(WorkingSet.objects.count(), 0)
