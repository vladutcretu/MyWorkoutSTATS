# Django
from django.test import TestCase

# App
from core.models import CustomUser
from fitness.models import MuscleGroup


class MuscleGroupsOnUserCreationTest(TestCase):
    """
    Test for signals.py - creating muscle groups for newly registered users
    """

    def test_default_muscle_groups_creation(self):
        """
        Test to see if newly registered users have all 8 default muscle groups
        """
        user = CustomUser.objects.create_user(
            username="testuser", email="test@mail.com", password="password123"
        )

        muscle_groups = MuscleGroup.objects.filter(user=user)
        self.assertEqual(muscle_groups.count(), 8)


class MuscleGroupModelTest(TestCase):
    """
    Tests for MuscleGroup model
    """

    def setUp(self):
        """
        Loading data pre-tests
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@mail.com", password="password123"
        )
        self.musclegroup = MuscleGroup.objects.create(
            user=self.user, name="Test Group"
        )

    def test_creation(self):
        """
        Test if new muscle group is correctly created
        """
        self.assertEqual(self.musclegroup.name, "Test Group")
        self.assertEqual(self.musclegroup.user, self.user)
        self.assertIsNotNone(self.musclegroup.created)

    def test_str_representation(self):
        """
        Test model's str method
        """
        expected_str = (
            f"Owner: {self.musclegroup.user} "
            f"- Muscle Group: {self.musclegroup.name}"
        )
        self.assertEqual(str(self.musclegroup), expected_str)

    def test_fields_max_length_validation(self):
        """
        Test max_length argument for fields
        """
        name = self.musclegroup.name * 31
        self.assertGreater(len(name), 30)

    def test_delete_user_then_deletes_musclegroups(self):
        """
        Test if after a user is deleted his muscle groups will be deleted
        as well
        """
        self.assertEqual(MuscleGroup.objects.count(), 9)
        self.user.delete()
        self.assertEqual(MuscleGroup.objects.count(), 0)
