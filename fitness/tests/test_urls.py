# Django
from django.test import TestCase
from django.urls import reverse

# App
from core.models import CustomUser
from fitness.models import (
    Workout,
    MuscleGroup,
    Exercise,
    WorkingSet,
    WorkoutComment,
)


class MuscleGroupUrlTest(TestCase):
    """
    Test musclegroup URLs
    """

    def setUp(self):
        """
        Load data pre-testing
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.edit_musclegroup_url = reverse(
            "edit-musclegroup", kwargs={"musclegroup_id": 1}
        )
        self.delete_musclegroup_url = reverse(
            "delete-musclegroup", kwargs={"musclegroup_id": 1}
        )

    def test_url_resolves_musclegroups_page(self):
        """
        Test musclegroups URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("musclegroups"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("musclegroups"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "musclegroups")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "musclegroups/view.html")

    def test_url_resolves_musclegroups_create_page(self):
        """
        Test musclegroups create URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("create-musclegroup"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("create-musclegroup"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(
            response.resolver_match.view_name, "create-musclegroup"
        )
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "musclegroups/create.html")

    def test_url_resolves_musclegroups_edit_page(self):
        """
        Test musclegroups edit URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.edit_musclegroup_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.edit_musclegroup_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "edit-musclegroup")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "musclegroups/create.html")

    def test_url_resolves_musclegroups_delete_page(self):
        """
        Test musclegroups delete URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.delete_musclegroup_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.delete_musclegroup_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(
            response.resolver_match.view_name, "delete-musclegroup"
        )
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "musclegroups/delete.html")


class ExerciseUrlTest(TestCase):
    """
    Test exercises URLs
    """

    def setUp(self):
        """
        Load data pre-testing
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.edit_exercise_url = reverse(
            "edit-exercise", kwargs={"exercise_id": 1}
        )
        self.delete_exercise_url = reverse(
            "delete-exercise", kwargs={"exercise_id": 1}
        )

    def test_url_resolves_exercises_page(self):
        """
        Test exercises URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("exercises"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("exercises"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "exercises")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "exercises/view.html")

    def test_url_resolves_exercises_create_page(self):
        """
        Test exercises create URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("create-exercise"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("create-exercise"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "create-exercise")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "exercises/create.html")

    def test_url_resolves_exercises_edit_page(self):
        """
        Test exercises edit URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.edit_exercise_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.edit_exercise_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "edit-exercise")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "exercises/create.html")

    def test_url_resolves_exercises_delete_page(self):
        """
        Test exercises delete URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.delete_exercise_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.delete_exercise_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "delete-exercise")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "exercises/delete.html")

    def test_url_resolves_exercises_collection_page(self):
        """
        Test exercises URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("collection-exercise"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("collection-exercise"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(
            response.resolver_match.view_name, "collection-exercise"
        )
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "exercises/collection.html")


class WorkoutUrlTest(TestCase):
    """
    Test workouts URLs
    """

    def setUp(self):
        """
        Load data pre-testing
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.workout = Workout.objects.create(
            user=self.user, name="Test Workout"
        )
        self.edit_workout_url = reverse(
            "edit-workout", kwargs={"workout_id": 1}
        )
        self.delete_workout_url = reverse(
            "delete-workout", kwargs={"workout_id": 1}
        )
        self.view_workout_url = reverse(
            "view-private-workout", kwargs={"workout_id": 1}
        )

    def test_url_resolves_workouts_page(self):
        """
        Test workouts URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("workouts"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("workouts"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "workouts")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workouts/view_all.html")

    def test_url_resolves_workouts_create_page(self):
        """
        Test workouts create URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("create-workout"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("create-workout"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "create-workout")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workouts/create.html")

    def test_url_resolves_workouts_edit_page(self):
        """
        Test workouts edit URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.edit_workout_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.edit_workout_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "edit-workout")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workouts/create.html")

    def test_url_resolves_workouts_delete_page(self):
        """
        Test workouts delete URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.delete_workout_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.delete_workout_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "delete-workout")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workouts/delete.html")

    def test_url_resolves_workouts_view_page(self):
        """
        Test workouts view URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.view_workout_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.view_workout_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(
            response.resolver_match.view_name, "view-private-workout"
        )
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workouts/view.html")


class ExerciseToWorkoutUrlTest(TestCase):
    """
    Test exercise to workout URLs
    """

    def setUp(self):
        """
        Load data pre-testing
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.workout = Workout.objects.create(
            user=self.user, name="Test Workout"
        )
        self.select_exercise_url = reverse(
            "select-exercise", kwargs={"workout_id": 1}
        )
        self.remove_exercise_url = reverse(
            "remove-exercise", kwargs={"exercise_id": 1}
        )

    def test_url_resolves_select_exercise_page(self):
        """
        Test select exercise URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.select_exercise_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.select_exercise_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "select-exercise")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(
            response, "exercise_to_workout/select_exercise.html"
        )

    def test_url_resolves_remove_exercise_page(self):
        """
        Test remove exercise URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.remove_exercise_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.remove_exercise_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "remove-exercise")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(
            response, "exercise_to_workout/remove_exercise.html"
        )


class WorkingSetsUrlTest(TestCase):
    """
    Test working sets URLs
    """

    def setUp(self):
        """
        Load data pre-testing
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.workout = Workout.objects.create(
            user=self.user, name="Test Workout"
        )
        self.musclegroup = MuscleGroup.objects.create(
            user=self.user, name="Test Group"
        )
        self.exercise = Exercise.objects.create(
            user=self.user, musclegroup=self.musclegroup, name="Test Exercise"
        )
        self.workingset = WorkingSet.objects.create(
            user=self.user,
            workout=self.workout,
            exercise=self.exercise,
        )
        self.create_set_url = reverse(
            "create-set", kwargs={"exercise_id": 1, "workout_id": 1}
        )
        self.edit_set_url = reverse("edit-set", kwargs={"workingset_id": 1})
        self.delete_set_url = reverse(
            "delete-set", kwargs={"workingset_id": 1}
        )

    def test_url_resolves_sets_page(self):
        """
        Test sets URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("sets"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("sets"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "sets")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workingsets/view.html")

    def test_url_resolves_workingsets_create_page(self):
        """
        Test workingsets create URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.create_set_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.create_set_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "create-set")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workingsets/create.html")

    def test_url_resolves_workingsets_edit_page(self):
        """
        Test workingsets edit URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.edit_set_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.edit_set_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "edit-set")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workingsets/edit.html")

    def test_url_resolves_workingsets_delete_page(self):
        """
        Test workingsets delete URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.delete_set_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.delete_set_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "delete-set")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "workingsets/delete.html")


class PublicWorkoutsUrlTest(TestCase):
    """
    Test public workouts URLs
    """

    def setUp(self):
        """Load data pre-testing"""
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.workout = Workout.objects.create(
            user=self.user, name="Test Workout"
        )
        self.view_public_workout_url = reverse(
            "view-public-workout", kwargs={"workout_id": 1}
        )

    def test_url_resolves_public_workouts_page(self):
        """
        Test public workouts URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("public-workouts"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("public-workouts"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "public-workouts")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "public_workouts/view_all.html")

    def test_url_resolves_view_public_workout_page(self):
        """
        Test view public workout URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.view_public_workout_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.view_public_workout_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(
            response.resolver_match.view_name, "view-public-workout"
        )
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "public_workouts/view.html")


class WorkoutCommentsUrlTest(TestCase):
    """
    Test workout comments URLs
    """

    def setUp(self):
        """
        Load data pre-testing
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.workout = Workout.objects.create(
            user=self.user, name="Test Workout"
        )
        self.workout_comment = WorkoutComment.objects.create(
            user=self.user, workout=self.workout, content="Test comment"
        )
        self.edit_commet_url = reverse(
            "edit-comment", kwargs={"workout_id": 1, "comment_id": 1}
        )
        self.delete_commet_url = reverse(
            "delete-comment", kwargs={"workout_id": 1, "comment_id": 1}
        )

    def test_url_resolves_edit_comment_page(self):
        """
        Test edit comment URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.edit_commet_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.edit_commet_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "edit-comment")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "comments/edit.html")

    def test_url_resolves_delete_comment_page(self):
        """
        Test delete comment URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(self.delete_commet_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.delete_commet_url)
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "delete-comment")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "comments/delete.html")


class AnalysisUrlTest(TestCase):
    """
    Test analysis URLs
    """

    def setUp(self):
        """
        Load data pre-testing
        """
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )

    def test_url_resolves_analyze_bodyweight_page(self):
        """
        Test body weight analysis URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("analyze-bodyweight"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("analyze-bodyweight"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(
            response.resolver_match.view_name, "analyze-bodyweight"
        )
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "analysis/bodyweight.html")

    def test_url_resolves_analyze_volume_page(self):
        """
        Test volume weight analysis URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("analyze-volume"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("analyze-volume"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "analyze-volume")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "analysis/volume.html")

    def test_url_resolves_analyze_records_page(self):
        """
        Test records weight analysis URL
        """
        # Test that anonymous users are redirected to login
        response = self.client.get(reverse("analyze-records"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        # Test that logged-in users can access the page
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("analyze-records"))
        self.assertEqual(response.status_code, 200)
        # Test if the URL uses the correct view
        self.assertEqual(response.resolver_match.view_name, "analyze-records")
        # Test if the URL renders the correct template
        self.assertTemplateUsed(response, "analysis/records.html")
