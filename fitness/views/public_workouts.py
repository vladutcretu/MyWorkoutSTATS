# Django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.cache import cache

# App
from fitness.models import Workout, WorkingSet, WorkoutComment


@login_required(login_url="login")
def view_public_workouts(request):
    """
    View used by user to see all public workouts of other users (his included),
    with search function by workout name and sorting options (by most recent
    created and number of likes).
    """
    # Get workouts from cache (if exists) or from database
    cache_key_public_workouts = f"view_public_workouts_{request.user.id}"
    public_workouts = cache.get(cache_key_public_workouts)
    if not public_workouts:
        public_workouts = Workout.objects.filter(public="yes").select_related(
            "user"
        )
        cache.set(cache_key_public_workouts, public_workouts, timeout=60 * 5)

    # Retrieve search query and sorting option from URL parameters
    q = request.GET.get("q", "")
    sort_by = request.GET.get(
        "sort", "created"
    )  # Default sorting by creation date

    # Filter by search query
    if q:
        public_workouts = public_workouts.filter(name__icontains=q)

    # Sorting logic
    if sort_by == "likes":
        # Sort by the number of likes (descending)
        public_workouts = public_workouts.annotate(
            total_likes=Count("likes")
        ).order_by("-total_likes")
    else:
        # Default sorting by created date (descending)
        public_workouts = public_workouts.order_by("-created")

    public_workouts_count = len(public_workouts)

    context = {
        "public_workouts": public_workouts,
        "public_workouts_count": public_workouts_count,
        "q": q,
        "sort_by": sort_by,
    }
    return render(request, "public_workouts/view_all.html", context)


@login_required(login_url="login")
def view_public_workout(request, workout_id):
    """
    View used by user to see a specific public workout
    """
    # Get workouts from cache (if exists) or from database
    cache_key_public_workout_workout = (
        f"view_public_workout_workout_{request.user.id}_{workout_id}"
    )
    public_workout = cache.get(cache_key_public_workout_workout)
    if not public_workout:
        public_workout = (
            Workout.objects.filter(pk=workout_id)
            .select_related("user")
            .annotate(like_count=Count("likes"))
            .first()
        )
        cache.set(
            cache_key_public_workout_workout, public_workout, timeout=60 * 5
        )

    # Get sets from cache (if exists) or from database
    cache_key_public_workout_workingsets = (
        f"view_public_workout_workingsets_{request.user.id}_{workout_id}"
    )
    public_workingsets = cache.get(cache_key_public_workout_workingsets)
    if not public_workingsets:
        public_workingsets = (
            WorkingSet.objects.filter(workout_exercise__workout=public_workout)
            .select_related(
                "workout_exercise__workout", "workout_exercise__exercise"
            )
            .order_by("id")
        )
        cache.set(
            cache_key_public_workout_workingsets,
            public_workingsets,
            timeout=60 * 5,
        )

    # Get comments from cache (if exists) or from database
    cache_key_public_workout_comments = (
        f"view_public_workout_comments_{request.user.id}_{workout_id}"
    )
    public_comments = cache.get(cache_key_public_workout_comments)
    if not public_comments:
        public_comments = WorkoutComment.objects.filter(
            workout=public_workout, parent=None
        ).select_related("user")
        cache.set(
            cache_key_public_workout_comments, public_comments, timeout=60 * 5
        )

    context = {
        "workout": public_workout,
        "workingsets": public_workingsets,
        "comments": public_comments,
    }
    return render(request, "public_workouts/view.html", context)
