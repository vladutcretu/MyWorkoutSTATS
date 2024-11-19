# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.models import MuscleGroup, Exercise, Workout, WorkoutExercise


class WorkoutModelTest(TestCase):
    """Tests for Workout and WorkoutExercise model"""
    def setUp(self):
        """Loading data pre-tests"""
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="mail1@test.com",
            password="testpass"
        )
        self.musclegroup = MuscleGroup.objects.create(
            user=self.user,
            name="Test Group"
        )
        self.exercise1 = Exercise.objects.create(
            user=self.user,
            musclegroup=self.musclegroup,
            name="Test Exercise 1"
        )
        self.exercise2 = Exercise.objects.create(
            user=self.user,
            musclegroup=self.musclegroup,
            name="Test Exercise 2"
        )
        self.workout = Workout.objects.create(
            user = self.user,
            name = "Test Workout",
            created = "2024-12-01"
        )
        self.workout_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise1,
            order = 1
        )

    def test_creation(self):
        """Test if new workout is correctly created"""
        self.assertEqual(self.workout.name, "Test Workout")
        self.assertEqual(self.workout.user, self.user)
        self.assertIsNone(self.workout.bodyweight)
        self.assertIsNone(self.workout.note)
        self.assertEqual(self.workout.public, "no")
        self.assertIsNotNone(self.workout.updated)
        self.assertIsNotNone(self.workout.created)
    
    def test_str_representation(self):
        """Test model's str method"""
        expected_str = f"Owner: {self.user} - Workout: {self.workout.name} - Date: {self.workout.created}"
        self.assertEqual(str(self.workout), expected_str)

    def test_exercise_is_in_workout(self):
        """Test if an exercise is associated with a workout"""
        self.assertTrue(self.workout.exercises.filter(id=self.exercise1.id).exists())

    def test_exercise_is_not_in_workout(self):
        """Test if an exercise is NOT associated with a workout"""
        self.assertFalse(self.workout.exercises.filter(id=self.exercise2.id).exists())
    
    def test_fields_max_length_validation(self):
        """Test max_length argument for fields"""
        name = self.workout.name * 31
        note = "a" * 101
        self.assertGreater(len(name), 30)
        self.assertGreater(len(note), 100)

    def test_delete_user_then_deletes_workouts(self):
        """Test if after a user is deleted his workouts will be deleted as well"""
        self.assertEqual(Workout.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Workout.objects.count(), 0)