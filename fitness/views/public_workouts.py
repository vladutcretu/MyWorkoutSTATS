# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# App
from fitness.models import Workout, WorkingSet, WorkoutComment


@login_required(login_url='login')
def view_public_workouts(request):
   """View used by user to see all public workouts of other users (his included),
   with search function by workout name and sorting options (by most recent created and number of likes)."""
   public_workouts = Workout.objects.filter(public="yes")
   public_workouts_count = public_workouts.count()

   # Retrieve search query and sorting option from URL parameters
   q = request.GET.get('q', '')
   sort_by = request.GET.get('sort', 'created')  # Default sorting by creation date

   # Filter by search query
   if q:
      public_workouts = public_workouts.filter(name__icontains=q)

   # Sorting logic
   if sort_by == 'likes':
      # Sort by the number of likes (descending)
      public_workouts = public_workouts.annotate(total_likes=Count('likes')).order_by('-total_likes')
   else:
      # Default sorting by created date (descending)
      public_workouts = public_workouts.order_by('-created')

   context = {
      'public_workouts': public_workouts,
      'public_workouts_count': public_workouts_count,
      'q': q,
      'sort_by': sort_by

   }
   return render(request, 'public_workouts/view_all.html', context)


@login_required(login_url='login')
def view_public_workout(request, workout_id):
   """View used by user to see a specific public workout"""
   workout = get_object_or_404(Workout, pk=workout_id)
   workingsets = WorkingSet.objects.filter().order_by('id')
   comments = WorkoutComment.objects.filter(workout=workout, parent=None)
   
   context = {
      'workout': workout,
      'workingsets': workingsets,
      'comments': comments
   }
   return render(request, 'public_workouts/view.html', context)