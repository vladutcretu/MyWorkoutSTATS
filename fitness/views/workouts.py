# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
from django.http import HttpResponse

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
    workouts = Workout.objects.filter(user=request.user)
    workouts_count = workouts.count()

    if request.user.is_authenticated:
        q = request.GET.get("q", "")
        workouts = Workout.objects.filter(
            Q(name__icontains=q), user=request.user
        )

        filter_by_created_date = request.GET.get("filter_by_created_date", "")
        if filter_by_created_date:
            workouts = workouts.filter(created=filter_by_created_date)

        filter_by_updated_date = request.GET.get("filter_by_updated_date", "")
        if filter_by_updated_date:
            workouts = workouts.filter(updated=filter_by_updated_date)

        filter_by_visibility = request.GET.get("filter_by_visibility", "")
        if filter_by_visibility:
            workouts = workouts.filter(public=filter_by_visibility)

        filter_by_bodyweight = request.GET.get("filter_by_bodyweight", "")
        if filter_by_bodyweight.isnumeric():
            # For integer values will be displayed results with floats number
            # but integer part equal to filtered value
            if filter_by_bodyweight.isdigit():
                workouts = workouts.filter(
                    bodyweight__icontains=int(filter_by_bodyweight)
                )
            else:
                workouts = workouts.filter(bodyweight=filter_by_bodyweight)

        workouts_count = workouts.count()
    else:
        workouts = []

    context = {"workouts": workouts, "workouts_count": workouts_count}

    return render(request, "workouts/view_all.html", context)


@login_required(login_url="login")
def create_workouts(request):
    """View used to create workout"""
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
        WorkoutExercise.objects.create(
            workout=new_workout, exercise=exercise, order=order
        )

        # Import workingsets from imported exercise
        import_workingsets(
            imported_exercise,
            imported_workout.created,
            request.user,
            new_workout,
            exercise,
            target_date,
        )

    return redirect(build_redirect_url(request, default_url=""))


@login_required(login_url="login")
def edit_workout(request, workout_id):
    """View used to edit fields from existing workout"""
    workout = Workout.objects.get(pk=workout_id, user=request.user)
    form = WorkoutForm(instance=workout)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect(build_redirect_url(request, default_url=""))

    context = {"form": form}
    return render(request, "workouts/create.html", context)


@login_required(login_url="login")
def delete_workout(request, workout_id):
    """View used to delete existing workout"""
    workout = get_object_or_404(Workout, pk=workout_id, user=request.user)

    if request.method == "POST":
        workout.delete()
        return redirect(build_redirect_url(request, default_url=""))

    context = {"workout": workout}
    return render(request, "workouts/delete.html", context)


@login_required(login_url="login")
def view_private_workout(request, workout_id):
    """View used by user to see a specific owned workout"""
    workout = get_object_or_404(Workout, pk=workout_id)
    workingsets = WorkingSet.objects.filter(user=request.user).order_by("id")

    context = {"workout": workout, "workingsets": workingsets}
    return render(request, "workouts/view.html", context)


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
    workout,
    exercise,
    created,
):
    """
    Creating (importing) workingsets of an exercise from an imported workout
    """
    for imported_workingset in imported_exercise.workingsets.filter(
        created=imported_workout_created
    ):
        WorkingSet.objects.create(
            user=user,
            workout=workout,
            exercise=exercise,
            weight=imported_workingset.weight,
            repetitions=imported_workingset.repetitions,
            distance=imported_workingset.distance,
            time=imported_workingset.time,
            created=created,
        )
