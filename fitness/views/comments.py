# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# App
from fitness.models import Workout, WorkoutComment
from fitness.forms import WorkoutCommentForm


@login_required(login_url='login')
def create_comment_or_reply(request, workout_id, parent_id=None):
   """View used to create either a comment or a reply to a comment for a public workout"""
   workout = get_object_or_404(Workout, pk=workout_id)
   parent_comment = None

   # Creating a reply to a comment if parent_id is provided
   if parent_id:
      parent_comment = get_object_or_404(WorkoutComment, pk=parent_id)

   if request.method == 'POST':
      comment_content = request.POST.get('comment')
      if len(comment_content) > 300:
         messages.error(request, 'Comment cannot exceed 300 characters.')
      else:
         # Create either a top-level comment or a reply
         WorkoutComment.objects.create(
               user=request.user,
               workout=workout,
               content=comment_content,
               parent=parent_comment  # This will be None for top-level comments
         )
         messages.success(request, 'Your comment has been added.')
      return redirect('view-public-workout', workout_id=workout.id)
   
   return redirect('view-public-workout', workout_id=workout.id)


@login_required(login_url='login')
def edit_comment(request, workout_id, comment_id):
   """View used to edit a specific self comment made by the user"""
   workout = get_object_or_404(Workout, pk=workout_id)
   comment = get_object_or_404(WorkoutComment, pk=comment_id, user=request.user)
   form = WorkoutCommentForm(instance=comment)

   if request.method == 'POST':
      form = WorkoutCommentForm(request.POST, instance=comment)
      if form.is_valid():
         form.save()
         return redirect('view-public-workout', workout_id=comment.workout.id)

   context = {
      'form': form,
      'workout': workout,
      'comment': comment
   }
   return render(request, 'comments/edit.html', context)


@login_required(login_url='login')
def delete_comment(request, workout_id, comment_id):
   """View used to delete a specific self comment made by the user"""
   workout = get_object_or_404(Workout, pk=workout_id)
   comment = get_object_or_404(WorkoutComment, pk=comment_id, user=request.user)

   if request.method == 'POST':
      comment.delete()
      return redirect('view-public-workout', workout_id=comment.workout.id)

   context = {
      'workout': workout,
      'comment': comment
   }
   return render(request, 'comments/delete.html', context)


@login_required(login_url='login')
def like_workout(request, workout_id):
   """View for liking or unliking a workout"""
   workout = get_object_or_404(Workout, pk=workout_id)

   if request.user in workout.likes.all():
      workout.likes.remove(request.user)
   else:
      workout.likes.add(request.user)

   return redirect('view-public-workout', workout_id=workout.id)