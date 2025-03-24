# Django
from django.test import TestCase

# App
from core.models import CustomUser
from core.forms import EditProfileForm


class EditProfileFormTest(TestCase):
    """
    Test EditProfileForm
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
            "profile_picture": None,
            "first_name": "Test",
            "last_name": "User",
            "age": 18,
            "city": "Test City",
            "bio": "This is a bio.",
            "instagram_url": "https://instagram.com/testuser",
        }

    def test_form_is_valid(self):
        """
        Test if form is valid with correct data
        """
        form = EditProfileForm(data=self.valid_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        user = CustomUser.objects.get(username="testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.age, 18)
        self.assertEqual(user.city, "Test City")
        self.assertEqual(user.bio, "This is a bio.")
        self.assertEqual(user.instagram_url, "https://instagram.com/testuser")
