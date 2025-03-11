# Django
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.core.cache import cache

# App
from core.models import CustomUser


class MainUrlTest(TestCase):
    """
    Test main URL
    """

    def test_url_resolves_main_page(self):
        """
        Test main URL
        """
        response = self.client.get(reverse("main"))
        # Test if the URL resolves correctly and returns status 200
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "main")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "main.html")


class UtilityUrlTest(TestCase):
    """
    Test utility URLs
    """

    @patch.object(cache, "set")
    @patch.object(cache, "get", return_value=None)
    def test_url_resolves_about_page(self, mock_cache_get, mock_cache_set):
        """
        Test about URL
        """
        response = self.client.get(reverse("about"))
        # Test if the URL resolves correctly and returns status 200
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "about")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "utility/about.html")

    @patch.object(cache, "set")
    @patch.object(cache, "get", return_value=None)
    def test_url_resolves_restapi_page(self, mock_cache_get, mock_cache_set):
        """
        Test rest api URL
        """
        response = self.client.get(reverse("rest-api"))
        # Test if the URL resolves correctly and returns status 200
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "rest-api")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "utility/rest_api.html")

    @patch.object(cache, "set")
    @patch.object(cache, "get", return_value=None)
    def test_url_resolves_help_page(self, mock_cache_get, mock_cache_set):
        """
        Test help URL
        """
        response = self.client.get(reverse("help"))
        # Test if the URL resolves correctly and returns status 200
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "help")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "utility/help.html")

    @patch.object(cache, "set")
    @patch.object(cache, "get", return_value=None)
    def test_url_resolves_privacy_page(self, mock_cache_get, mock_cache_set):
        """
        Test privacy URL
        """
        response = self.client.get(reverse("privacy"))
        # Test if the URL resolves correctly and returns status 200
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "privacy")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "utility/privacy.html")


class AuthUrlTest(TestCase):
    """
    Test auth URLs
    """

    def setUp(self):
        """Load data pre-testing"""
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )

    def test_url_resolves_login_page(self):
        """
        Test login URL
        """
        response = self.client.get(reverse("login"))
        # Test if the URL resolves correctly and returns status 200
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "login")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "auth/login.html")
        # Test that logged in users can NOT access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)

    def test_url_resolves_logout_page(self):
        """
        Test logout URL
        """
        response = self.client.get(reverse("logout"))
        # Test if the URL resolves correctly and returns status 302 - main
        self.assertEqual(response.status_code, 302)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "logout")

    def test_url_resolves_signup_page(self):
        """
        Test signup URL
        """
        response = self.client.get(reverse("signup"))
        # Test if the URL resolves correctly and returns status 200
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "signup")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "auth/signup.html")

    def test_url_resolves_recover_page(self):
        """
        Test recover URL
        """
        response = self.client.get(reverse("recover"))
        # Test if the URL resolves correctly and returns status 200
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "recover")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "auth/recover.html")

    def test_url_resolves_change_password_page(self):
        """
        Test change password URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("change-password"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("change-password"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "change-password")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "auth/change_password.html")

    def test_url_resolves_delete_account_page(self):
        """
        Test delete account URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("delete-account"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("delete-account"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "delete-account")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "auth/delete_account.html")


class UserUrlTest(TestCase):
    """
    Test user URLs
    """

    def setUp(self):
        """Load data pre-testing"""
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.profile_url = reverse("profile", kwargs={"user_id": self.user.id})

    @patch.object(cache, "set")
    @patch.object(cache, "get", return_value=None)
    def test_url_resolves_account_page(self, mock_cache_get, mock_cache_set):
        """
        Test account URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "account")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "user/account.html")

    def test_url_resolves_profile_page(self):
        """
        Test profile URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        # # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "profile")
        # # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "user/profile.html")

    def test_url_resolves_edit_profile_page(self):
        """
        Test edit profile URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("edit-profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("edit-profile"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "edit-profile")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "user/edit_profile.html")
