# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache

# App
from fitness.models import Workout, WorkoutComment
from fitness.forms import WorkoutCommentForm


@login_required(login_url="login")
def create_comment_or_reply(request, workout_id, parent_id=None):
    """
    View used to create either a comment or a reply to a comment for a
    public workout
    """
    workout = get_object_or_404(Workout, pk=workout_id)
    parent_comment = None

    # Creating a reply to a comment if parent_id is provided
    if parent_id:
        parent_comment = get_object_or_404(WorkoutComment, pk=parent_id)

    if request.method == "POST":
        comment_content = request.POST.get("comment")
        if len(comment_content) > 300:
            messages.error(request, "Comment cannot exceed 300 characters.")
        else:
            # Create either a top-level comment or a reply
            WorkoutComment.objects.create(
                user=request.user,
                workout=workout,
                content=comment_content,
                parent=parent_comment,  # This will be None for top-level comms
            )
            messages.success(request, "Your comment has been added.")

        # Once create a comment invalidate public workout cache
        cache_key_public_workout_comments = (
            f"view_public_workout_comments_{request.user.id}_{workout_id}"
        )
        cache.delete(cache_key_public_workout_comments)

        return redirect("view-public-workout", workout_id=workout.id)

    return redirect("view-public-workout", workout_id=workout.id)


@login_required(login_url="login")
def edit_comment(request, workout_id, comment_id):
    """
    View used to edit a specific self comment made by the user
    """
    workout = get_object_or_404(Workout, pk=workout_id)
    comment = get_object_or_404(
        WorkoutComment, pk=comment_id, user=request.user
    )
    form = WorkoutCommentForm(instance=comment)

    if request.method == "POST":
        form = WorkoutCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()

            # Once edit a comment invalidate public workout cache
            cache_key_public_workout_comments = (
                f"view_public_workout_comments_{request.user.id}_{workout_id}"
            )
            cache.delete(cache_key_public_workout_comments)

            return redirect(
                "view-public-workout", workout_id=comment.workout.id
            )

    context = {"form": form, "workout": workout, "comment": comment}
    return render(request, "comments/edit.html", context)


@login_required(login_url="login")
def delete_comment(request, workout_id, comment_id):
    """
    View used to delete a specific self comment made by the user
    """
    workout = get_object_or_404(Workout, pk=workout_id)
    comment = get_object_or_404(
        WorkoutComment, pk=comment_id, user=request.user
    )

    if request.method == "POST":
        comment.delete()

        # Once delete a comment invalidate public workout cache
        cache_key_public_workout_comments = (
            f"view_public_workout_comments_{request.user.id}_{workout_id}"
        )
        cache.delete(cache_key_public_workout_comments)

        return redirect("view-public-workout", workout_id=comment.workout.id)

    context = {"workout": workout, "comment": comment}
    return render(request, "comments/delete.html", context)


@login_required(login_url="login")
def like_workout(request, workout_id):
    """
    View for liking or unliking a workout
    """
    workout = get_object_or_404(Workout, pk=workout_id)

    if request.user in workout.likes.all():
        workout.likes.remove(request.user)
    else:
        workout.likes.add(request.user)

    # Once like/unlike a public workout invalidate public workouts cache
    cache_key_public_workouts = f"view_public_workouts_{request.user.id}"
    cache.delete(cache_key_public_workouts)
    cache_key_public_workout_workout = (
        f"view_public_workout_workout_{request.user.id}_{workout_id}"
    )
    cache.delete(cache_key_public_workout_workout)

    return redirect("view-public-workout", workout_id=workout.id)
