# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.cache import cache

# App
from fitness.models import WorkoutExercise, Exercise, WorkingSet
from fitness.forms import WorkingSetForm
from core.views.main import build_redirect_url


@login_required(login_url="login")
def view_sets(request):
    """
    View used by user to see all sets, with filter options
    """
    # Get sets from cache (if exists) or from database
    cache_key_workingsets = f"view_sets_workingsets{request.user.id}"
    workingsets = cache.get(cache_key_workingsets)
    if not workingsets:
        workingsets = WorkingSet.objects.filter(
            user=request.user
        ).select_related(
            "workout_exercise__exercise", "workout_exercise__workout"
        )
        cache.set(cache_key_workingsets, workingsets, timeout=60 * 60)

    # Get exercises from cache (if exists) or from database
    cache_key_exercises = f"view_sets_exercises_{request.user.id}"
    exercises = cache.get(cache_key_exercises)
    if not exercises:
        exercises = Exercise.objects.filter(user=request.user)
        cache.set(cache_key_exercises, exercises, timeout=60 * 60)

    # Filter sets by his fields values
    filter_by_created_date = request.GET.get("filter_by_created_date", "")
    if filter_by_created_date:
        workingsets = [
            ws
            for ws in workingsets
            if ws.workout_exercise.workout.created.strftime("%Y-%m-%d")
            == filter_by_created_date
        ]

    filter_by_exercise = request.GET.get("filter_by_exercise", "")
    if filter_by_exercise:
        workingsets = [
            ws
            for ws in workingsets
            if ws.workout_exercise.exercise.id == int(filter_by_exercise)
        ]

    filter_by_type = request.GET.get("filter_by_type", "")
    if filter_by_type:
        workingsets = [ws for ws in workingsets if ws.type == filter_by_type]

    workingsets_count = len(workingsets)

    context = {
        "workingsets": workingsets,
        "workingsets_count": workingsets_count,
        "exercises": exercises,
    }
    return render(request, "workingsets/view.html", context)


@login_required(login_url="login")
def create_sets(request, exercise_id, workout_id):
    """
    View used to add working set to an existing exercise in a workout
    """
    # exercise = Exercise.objects.get(pk=exercise_id, user=request.user)
    # workout = Workout.objects.get(pk=workout_id, user=request.user)
    workout_exercise = WorkoutExercise.objects.get(
        exercise_id=exercise_id, workout_id=workout_id
    )

    target_date = request.COOKIES.get("targetDate", date.today())

    if request.method == "POST":
        type_weight = request.POST.get("type_weight")
        type_endurance = request.POST.get("type_endurance")
        repetitions = request.POST.get("repetitions")
        weight = request.POST.get("weight")
        distance = request.POST.get("distance")
        time = request.POST.get("time")

        WorkingSet.objects.create(
            user=request.user,
            workout_exercise=workout_exercise,
            type=type_weight if weight else type_endurance,
            repetitions=repetitions if repetitions else None,
            weight=weight if weight else None,
            distance=distance if distance else None,
            time=time if time else None,
            created=target_date,
        )

        return redirect(build_redirect_url(request, default_url=""))

    # context = {"exercise": exercise, "workout": workout}
    context = {"workout_exercise": workout_exercise}
    return render(request, "workingsets/create.html", context)


@login_required(login_url="login")
def copy_sets(request, workingset_id):
    """
    View used to duplicate a working set already created for an exercise in
    a workout
    """
    workingset = get_object_or_404(
        WorkingSet, pk=workingset_id, user=request.user
    )

    WorkingSet.objects.create(
        user=request.user,
        workout=workingset.workout,
        exercise=workingset.exercise,
        type=workingset.type,
        repetitions=workingset.repetitions,
        weight=workingset.weight,
        distance=workingset.distance,
        time=workingset.time,
        created=workingset.created,
    )

    return redirect(build_redirect_url(request, default_url=""))


@login_required(login_url="login")
def edit_sets(request, workingset_id):
    """
    View used to edit values of existing working set
    """
    workingset = get_object_or_404(
        WorkingSet, pk=workingset_id, user=request.user
    )
    form = WorkingSetForm(instance=workingset)

    if request.method == "POST":
        form = WorkingSetForm(request.POST, instance=workingset)
        if form.is_valid():
            form.save()
            return redirect(build_redirect_url(request, default_url=""))

    context = {"form": form}
    return render(request, "workingsets/edit.html", context)


@login_required(login_url="login")
def delete_sets(request, workingset_id):
    """
    View used to delete working set from an existing exercise in a workout
    """
    workingset = get_object_or_404(
        WorkingSet, pk=workingset_id, user=request.user
    )

    if request.method == "POST":
        workingset.delete()
        return redirect(build_redirect_url(request, default_url=""))

    context = {"workingset": workingset}
    return render(request, "workingsets/delete.html", context)
