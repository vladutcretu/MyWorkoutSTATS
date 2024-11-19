# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# App
from fitness.models import Workout, WorkoutExercise, Exercise, WorkingSet, MuscleGroup
from core.views.main import build_redirect_url


@login_required(login_url='login')
def select_exercise(request, workout_id):
   """View used to display all exercises with their muscle groups, with option of search exercise by name or filter by muscle group"""
   if request.user.is_authenticated:
      q = request.GET.get('q', '')
      exercises = Exercise.objects.filter(
         Q(musclegroup__name__icontains = q) |
         Q(name__icontains = q),
         user=request.user
         )
      musclegroups = MuscleGroup.objects.filter(user=request.user)
   else:
      exercises = []
      musclegroups = []

   exercises_count = exercises.count()
   workout = Workout.objects.get(pk=workout_id)

   context = {
      'exercises': exercises,
      'exercises_count': exercises_count,
      'musclegroups': musclegroups,
      'workout': workout
   }
   return render(request, 'exercise_to_workout/select_exercise.html', context)


@login_required(login_url='login')
def add_exercise_to_workout(request, exercise_id, workout_id):
   """View to add an exercise to a specific workout"""
   workout = Workout.objects.get(pk=workout_id)
   exercise = Exercise.objects.get(pk=exercise_id)

   # Exercises order in workout according to the order of their addition by the user
   order = workout.exercises.count() + 1

   # Add exercise to workout with their order using WorkoutExercise (models.py) created for this
   workout_exercise = WorkoutExercise.objects.create(workout=workout, exercise=exercise, order=order)
   
   return redirect(build_redirect_url(request, default_url=''))


@login_required(login_url='login')
def remove_exercise_from_workout(request, exercise_id):
   """View used to remove an exercise from a specific workout"""
   exercise = get_object_or_404(Exercise, pk=exercise_id, user=request.user)

   if request.method == "POST":
      workouts_with_exercise = Workout.objects.filter(exercises=exercise, user=request.user)

      # Work with the first workout with this exercise
      if workouts_with_exercise.exists():
         workout = workouts_with_exercise.first()

         # Delete associated working sets for the exercise removed
         working_sets_to_delete = WorkingSet.objects.filter(exercise=exercise, user=request.user)
         working_sets_to_delete.delete()

         # Remove exercise from the workout
         workout.exercises.remove(exercise)

         return redirect(build_redirect_url(request, default_url=''))
   
   context = {
      'exercise': exercise
   }
   return render(request, 'exercise_to_workout/remove_exercise.html', context)