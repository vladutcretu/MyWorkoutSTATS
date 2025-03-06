# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
import requests

# App
from fitness.models import Exercise, MuscleGroup
from fitness.forms import ExerciseForm


@login_required(login_url="login")
def view_exercises(request):
    """
    View used by user to see all exercises, with search them by their name or
    filter by muscle group options
    """
    exercises = Exercise.objects.filter(user=request.user)
    exercises_count = exercises.count()
    musclegroups = MuscleGroup.objects.filter(user=request.user)

    if request.user.is_authenticated:
        q = request.GET.get("q", "")
        exercises = Exercise.objects.filter(
            Q(musclegroup__name__icontains=q) | Q(name__icontains=q),
            user=request.user,
        )

        filter_by_musclegroup = request.GET.get("filter_by_musclegroup", "")
        if filter_by_musclegroup:
            exercises = exercises.filter(musclegroup=filter_by_musclegroup)

        exercises_count = exercises.count()
    else:
        exercises = []

    context = {
        "exercises": exercises,
        "exercises_count": exercises_count,
        "musclegroups": musclegroups,
    }
    return render(request, "exercises/view.html", context)


@login_required(login_url="login")
def create_exercises(request):
    """View used to create exercise"""
    if request.method == "POST":
        form = ExerciseForm(request.user, request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            return redirect("exercises")
    else:
        form = ExerciseForm(request.user)

    context = {"form": form}
    return render(request, "exercises/create.html", context)


@login_required(login_url="login")
def edit_exercises(request, exercise_id):
    """View used to edit fields from existing muscle group"""
    exercise = get_object_or_404(Exercise, pk=exercise_id, user=request.user)
    form = ExerciseForm(instance=exercise, user=request.user)

    if request.method == "POST":
        form = ExerciseForm(request.user, request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect("exercises")

    context = {"form": form}
    return render(request, "exercises/create.html", context)


@login_required(login_url="login")
def delete_exercises(request, exercise_id):
    """View used to delete exercise"""
    exercise = get_object_or_404(Exercise, pk=exercise_id, user=request.user)

    if request.method == "POST":
        exercise.delete()
        return redirect("exercises")

    context = {"exercise": exercise}
    return render(request, "exercises/delete.html", context)


@login_required(login_url="login")
def collection_exercises(request):
    """
    View used to show muscle groups and exercises from WGER API:
    https://wger.de/en/software/api
    """
    # Auth credentials
    username = settings.WGER_API_USERNAME
    password = settings.WGER_API_PASSWORD

    # Set by default category to None for initial page view
    musclegroup_id = None

    # Get category ID from POST request
    if request.method == "POST":
        musclegroup_id = request.POST.get("musclegroup_id")

    # Get musclegroups list from the API
    musclegroups = fetch_WGER_musclegroups_data(username, password)

    # Get exercises list from the API
    exercises = (
        fetch_WGER_exercises_data(username, password, musclegroup_id)
        if musclegroup_id
        else []
    )

    context = {"musclegroups": musclegroups, "exercises": exercises}
    return render(request, "exercises/collection.html", context)


# # # # # # WGER API VIEWS # # # # # #
def get_WGER_token_and_auth(username, password):
    """
    Get the access token and make authentication to WGER API:
    https://wger.de/en/software/api
    """
    # Get token using credentials
    auth_response = requests.post(
        "https://wger.de/api/v2/token",
        data={"username": username, "password": password},
    )

    if auth_response.status_code != 200:
        return f"Error on authentication: {auth_response.status_code}"

    tokens = auth_response.json()
    access_token = tokens.get("access")

    if not access_token:
        return "Access token can't be obtained."

    # Check token
    verify_response = requests.post(
        "https://wger.de/api/v2/token/verify", data={"token": access_token}
    )

    if verify_response.status_code != 200:
        return (
            f"Access token is invalid or expired:"
            f"{verify_response.status_code}"
        )

    # print(f"Acces token is valid: {verify_response.status_code}")
    return access_token


def fetch_WGER_paginated_data(url, headers, process_function):
    """
    Parse paginated results and collect all data using `process_function`.
    """
    all_items = []

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"Error on getting data: {response.status_code}"

        data = response.json()
        items = process_function(data)
        all_items.extend(items)

        url = data.get("next")
        # print(f"Next page url: {url}")

    return all_items


def fetch_WGER_musclegroups_data(username, password):
    """Get data for musclegroups."""
    access_token = get_WGER_token_and_auth(username, password)

    if not access_token:
        return "Access token is invalid or expired."

    url = "https://wger.de/api/v2/exercisecategory/"
    headers = {"Authorization": f"Bearer {access_token}"}

    return fetch_WGER_paginated_data(url, headers, get_WGER_musclegroups)


def get_WGER_musclegroups(data):
    """Get data for every musclegroup."""
    return [
        (musclegroup.get("id"), musclegroup.get("name"))
        for musclegroup in data.get("results", [])
    ]


def fetch_WGER_exercises_data(username, password, category):
    """Get data for exercises"""
    access_token = get_WGER_token_and_auth(username, password)

    if not access_token:
        return "Access token is invalid or expired."

    url = (
        f"https://wger.de/api/v2/exercise/"
        f"?category={category}&language=2&limit=20"
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    return fetch_WGER_paginated_data(url, headers, get_WGER_exercises)


def get_WGER_exercises(data):
    """Get data for every exercise."""
    return [
        (exercise.get("name"), exercise.get("description"))
        for exercise in data.get("results", [])
    ]
