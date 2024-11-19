# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.models import Workout, WorkoutComment


class WorkoutCommentModelTest(TestCase):
    """Tests for WorkoutComment model"""
    def setUp(self):
        """Loading data pre-tests"""
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="mail1@test.com",
            password="testpass"
        )
        self.workout = Workout.objects.create(
            user = self.user,
            name = "Test Workout",
            created = "2024-12-01"
        )
        self.workout_comment = WorkoutComment.objects.create(
            user=self.user,
            workout=self.workout,
            content='abc',
        )

    def test_creation(self):
        """Test if new comment is correctly created"""
        self.assertEqual(self.workout_comment.user, self.user)
        self.assertEqual(self.workout_comment.workout, self.workout)
        self.assertEqual(self.workout_comment.content, 'abc')
        self.assertIsNone(self.workout_comment.parent)
        self.assertIsNotNone(self.workout_comment.updated)
        self.assertIsNotNone(self.workout_comment.created)

    def test_str_representation(self):
        """Test model's str method"""
        expected_str = f"{self.workout} - {self.user.username}: {self.workout_comment.content[:30]}..."
        self.assertEqual(str(self.workout_comment), expected_str)

    def test_fields_max_length_validation(self):
        """Test max_length argument for fields"""
        content = 'a' * 301
        self.assertGreater(len(content), 300)
    
    def test_delete_user_then_deletes_comments(self):
        """Test if after a user is deleted his comments will be deleted as well"""
        self.assertEqual(WorkoutComment.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Workout.objects.count(), 0)

    def test_delete_workout_then_deletes_comments(self):
        """Test if after a workout is deleted his comments will be deleted as well"""
        self.assertEqual(WorkoutComment.objects.count(), 1)
        self.workout.delete()
        self.assertEqual(WorkoutComment.objects.count(), 0)

    def test_comment_parent(self):
        """Test if new comment is correctly created as a child to a parent comment"""
        workout_comment_child = WorkoutComment.objects.create(
            user=self.user,
            workout=self.workout,
            content='def',
            parent=self.workout_comment
        )
        self.assertEqual(workout_comment_child.user, self.user)
        self.assertEqual(workout_comment_child.workout, self.workout)
        self.assertEqual(workout_comment_child.content, 'def')
        self.assertEqual(workout_comment_child.parent, self.workout_comment)
        self.assertIsNotNone(workout_comment_child.updated)
        self.assertIsNotNone(workout_comment_child.created)

        # Test if delete the parent comment the child will be deleted as well
        self.assertEqual(WorkoutComment.objects.count(), 2)
        self.workout_comment.delete()
        self.assertEqual(WorkoutComment.objects.count(), 0)