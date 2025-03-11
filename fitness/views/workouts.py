# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import HttpResponse
from django.core.cache import cache

# App
from fitness.models import (
    Workout,
    WorkoutExercise,
    Exercise,
    WorkingSet,
    MuscleGroup,
)
from fitness.forms import WorkoutForm
from core.views.main import build_redirect_url


@login_required(login_url="login")
def view_workouts(request):
    """
    View used by user to see all his workouts, with search function by workout
    name or filter function to find a specific one(s)"""
    # Get workouts from cache (if exists) or from database
    cache_key_workouts = f"view_workouts_{request.user.id}"
    workouts = cache.get(cache_key_workouts)
    if not workouts:
        workouts = Workout.objects.filter(user=request.user)
        cache.set(cache_key_workouts, workouts, timeout=60 * 60)

    # Filter workouts by his fields values
    filter_by_created_date = request.GET.get("filter_by_created_date", "")
    if filter_by_created_date:
        workouts = [
            w
            for w in workouts
            if w.created.strftime("%Y-%m-%d") == filter_by_created_date
        ]

    filter_by_updated_date = request.GET.get("filter_by_updated_date", "")
    if filter_by_updated_date:
        workouts = [
            w
            for w in workouts
            if w.updated.strftime("%Y-%m-%d") == filter_by_updated_date
        ]

    filter_by_visibility = request.GET.get("filter_by_visibility", "")
    if filter_by_visibility:
        workouts = [
            w for w in workouts if str(w.public) == filter_by_visibility
        ]

    filter_by_bodyweight = request.GET.get("filter_by_bodyweight", "")
    if filter_by_bodyweight:
        try:
            bodyweight_filter = float(filter_by_bodyweight)
            workouts = [
                w for w in workouts if w.bodyweight == bodyweight_filter
            ]
        except ValueError:
            pass

    # Filter exercises based on search query
    q = request.GET.get("q", "")
    if q:
        workouts = [w for w in workouts if q.lower() in w.name.lower()]

    workouts_count = len(workouts)

    context = {"workouts": workouts, "workouts_count": workouts_count}

    return render(request, "workouts/view_all.html", context)


@login_required(login_url="login")
def create_workouts(request):
    """
    View used to create workout
    """
    # Import cookie to use same target_data as the workout shown in main page
    # (to create workout with the same date as date selected)
    target_date = request.COOKIES.get("targetDate", date.today())
    existing_workout = Workout.objects.filter(
        user=request.user, created=target_date
    )

    if existing_workout:
        return HttpResponse(
            "You already have a workout created for this day."
            "Delete it before creating another."
        )

    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.created = target_date
            workout.save()

            # Once create a workout invalidate workout cache
            cache_key_workouts = f"view_workouts_{request.user.id}"
            cache.delete(cache_key_workouts)

            return redirect(build_redirect_url(request, default_url=""))
    else:
        form = WorkoutForm()

    context = {"form": form}
    return render(request, "workouts/create.html", context)


@login_required(login_url="login")
def import_workouts(request, workout_id):
    """
    View used to import a workout (copy exercises and workingsets), owned by
    user or public one
    """
    # Import cookie to use same target_data as the workout shown in main page
    # (to create workout with the same date as date selected)
    target_date = request.COOKIES.get("targetDate", date.today())
    existing_workout = Workout.objects.filter(
        user=request.user, created=target_date
    ).exists()

    if existing_workout:
        return HttpResponse(
            "You already have a workout created for this day."
            "Delete it before creating another."
        )

    # Get the workout to be imported
    imported_workout = get_object_or_404(Workout, pk=workout_id)

    # Create a new workout for user
    new_workout = Workout.objects.create(
        user=request.user, name=imported_workout.name, created=target_date
    )

    # Import exercises to workout
    for order, imported_exercise in enumerate(
        imported_workout.exercises.all(), start=1
    ):
        # Create exercise or use existing one
        exercise = get_or_create_musclegroup_and_exercise(
            imported_exercise, request.user
        )

        # Add exercise to newly imported workout
        workout_exercise = WorkoutExercise.objects.create(
            workout=new_workout, exercise=exercise, order=order
        )

        # Import workingsets from imported exercise
        import_workingsets(
            imported_exercise,
            imported_workout.created,
            request.user,
            workout_exercise,
            target_date,
        )

    # Once import a workout invalidate workout cache
    cache_key_workouts = f"view_workouts_{request.user.id}"
    cache.delete(cache_key_workouts)

    return redirect(build_redirect_url(request, default_url=""))


def get_or_create_musclegroup_and_exercise(imported_exercise, user):
    """
    Get musclegroup and exercise from imported workout or create if user
    does not have it
    """
    musclegroup, _ = MuscleGroup.objects.get_or_create(
        user=user,
        name=imported_exercise.musclegroup.name,
        defaults={"created": date.today()},
    )
    exercise, _ = Exercise.objects.get_or_create(
        user=user,
        name=imported_exercise.name,
        musclegroup=musclegroup,
        defaults={"created": date.today()},
    )
    return exercise


def import_workingsets(
    imported_exercise,
    imported_workout_created,
    user,
    workout_exercise,
    created,
):
    """
    Creating (importing) workingsets of an exercise from an imported workout
    """
    # Get sets associated of every exercise from imported workout
    imported_workoutsets = WorkingSet.objects.filter(
        workout_exercise__exercise=imported_exercise,
        workout_exercise__workout__created=imported_workout_created,
    )

    # Import sets to newly created workout
    for imported_workingset in imported_workoutsets:
        WorkingSet.objects.create(
            user=user,
            workout_exercise=workout_exercise,
            weight=imported_workingset.weight,
            repetitions=imported_workingset.repetitions,
            distance=imported_workingset.distance,
            time=imported_workingset.time,
            created=created,
        )


@login_required(login_url="login")
def edit_workout(request, workout_id):
    """
    View used to edit fields from existing workout
    """
    workout = Workout.objects.get(pk=workout_id, user=request.user)
    form = WorkoutForm(instance=workout)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()

            # Once edit a workout invalidate workout cache
            cache_key_workouts = f"view_workouts_{request.user.id}"
            cache.delete(cache_key_workouts)
            cache_key_private_workout = (
                f"view_private_workouts_workout_{request.user.id}_{workout_id}"
            )
            cache.delete(cache_key_private_workout)
            cache_key_private_workingsets = (
                f"view_private_workouts_workingsets_"
                f"{request.user.id}_{workout_id}"
            )
            cache.delete(cache_key_private_workingsets)
            cache_key_private_musclegroups = (
                f"view_private_workouts_musclegroups_"
                f"{request.user.id}_{workout_id}"
            )
            cache.delete(cache_key_private_musclegroups)

            return redirect(build_redirect_url(request, default_url=""))

    context = {"form": form}
    return render(request, "workouts/create.html", context)


@login_required(login_url="login")
def delete_workout(request, workout_id):
    """
    View used to delete existing workout
    """
    workout = get_object_or_404(Workout, pk=workout_id, user=request.user)

    if request.method == "POST":
        workout.delete()

        # Once delete a workout invalidate workout cache
        cache_key_workouts = f"view_workouts_{request.user.id}"
        cache.delete(cache_key_workouts)
        cache_key_private_workout = (
            f"view_private_workouts_workout_{request.user.id}_{workout_id}"
        )
        cache.delete(cache_key_private_workout)
        cache_key_private_workingsets = (
            f"view_private_workouts_workingsets_{request.user.id}_{workout_id}"
        )
        cache.delete(cache_key_private_workingsets)
        cache_key_private_musclegroups = (
            f"view_private_workouts_musclegroups_"
            f"{request.user.id}_{workout_id}"
        )
        cache.delete(cache_key_private_musclegroups)

        return redirect(build_redirect_url(request, default_url=""))

    context = {"workout": workout}
    return render(request, "workouts/delete.html", context)


@login_required(login_url="login")
def view_private_workout(request, workout_id):
    """
    View used by user to see a specific owned workout
    """
    # Get workouts from cache (if exists) or from database
    cache_key_private_workout = (
        f"view_private_workouts_workout_{request.user.id}_{workout_id}"
    )
    workout = cache.get(cache_key_private_workout)
    if not workout:
        workout = get_object_or_404(Workout, pk=workout_id)
        cache.set(cache_key_private_workout, workout, timeout=60 * 60)

    # Get workingsets from cache (if exists) or from database
    cache_key_private_workingsets = (
        f"view_private_workouts_workingsets_{request.user.id}_{workout_id}"
    )
    workingsets = cache.get(cache_key_private_workingsets)
    if not workingsets:
        workingsets = (
            WorkingSet.objects.filter(
                user=request.user, workout_exercise__workout=workout
            )
            .select_related("workout_exercise__exercise__musclegroup")
            .order_by("id")
        )
        cache.set(cache_key_private_workingsets, workingsets, timeout=60 * 60)

    # Get musclegroups from cache (if exists) or from database
    cache_key_private_musclegroups = (
        f"view_private_workouts_musclegroups_{request.user.id}_{workout_id}"
    )
    musclegroups = cache.get(cache_key_private_musclegroups)
    if not musclegroups:
        musclegroups = MuscleGroup.objects.filter(user=request.user)
        cache.set(
            cache_key_private_musclegroups, musclegroups, timeout=60 * 60
        )

    context = {
        "workout": workout,
        "workingsets": workingsets,
        "musclegroups": musclegroups,
    }
    return render(request, "workouts/view.html", context)
