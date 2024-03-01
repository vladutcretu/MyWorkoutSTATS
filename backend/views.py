from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse

import requests
from datetime import date, timedelta

from .models import MuscleGroup, Exercise, WorkingSet, Workout, WorkoutExercise
from .forms import MuscleGroupForm, ExerciseForm, WorkingSetForm, WorkoutForm


# Create your views here.

def loginPage(request):
   """View for Login page"""
   if request.method == 'POST':
      username = request.POST.get('username').lower()
      password = request.POST.get('password')

      try: 
         user = User.objects.get(username=username)
      except:
         messages.error(request, "User does not exist")

      user = authenticate(request, username=username, password=password)

      if user is not None:
         login(request, user)
         return redirect('home')
      else:
         messages.error(request, "Password is incorrect")

   context = {

   }
   return render(request, 'backend/login.html', context)


def logoutPage(request):
   """View for Logout page"""
   logout(request)
   return redirect('home')


def registerPage(request):
   """View for Register page""" 
   if request.user.is_authenticated:
      return redirect('home')

   form = UserCreationForm()
   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('home')
      else:
         messages.error(request, "Something bad happened. Try again please!")

   context = {
      'form': form
   }
   return render (request, 'backend/register.html', context)


def homePage(request):
   """View used by API get to display in home page the correct workout based by user actions"""

   # Obtain days_diff value from query string
   days_diff = int(request.GET.get('days_diff', 0))

   # Calculate the date for the desired day based on days_diff value (output is YYYY-MM-DD)
   target_date = date.today() + timedelta(days=int(days_diff))
   target_date_str = target_date.strftime('%Y-%m-%d')

   # API call
   api_url = reverse('get_workouts')
   response = requests.get(request.build_absolute_uri(api_url))
   workouts = response.json()

   # Obtain in page only the workout that user wants
   workout_filtered = [workout for workout in workouts if workout['user'] == request.user.id and workout['created'] == target_date_str]

   context = {
      'workouts': workout_filtered,
      'target_date': target_date,
   }

   # Add days_diff & target_date in cookies to use it in other pages
   response = render(request, 'backend/home.html', context)
   response.set_cookie('daysDiff', days_diff)
   response.set_cookie('targetDate', str(target_date))
   return response


@login_required(login_url='login')
def userAccount(request):
   """View for User Account page"""

   context = {

   }
   return render(request, 'backend/account.html', context)


@login_required(login_url='login')
def workouts(request):
   """View used by user to see all his workouts, with search function by workout name or filter function to find a specific one(s)"""
   workouts = Workout.objects.filter(user=request.user)
   workouts_count = workouts.count()

   if request.user.is_authenticated:
      q = request.GET.get('q', '')
      workouts = Workout.objects.filter(
         Q(name__icontains = q),
         user=request.user
      )

      filter_by_created_date = request.GET.get('filter_by_created_date', '')
      if filter_by_created_date:
         workouts = workouts.filter(created=filter_by_created_date)

      filter_by_updated_date = request.GET.get('filter_by_updated_date', '')
      if filter_by_updated_date:
         workouts = workouts.filter(updated=filter_by_updated_date)

      filter_by_visibility = request.GET.get('filter_by_visibility', '')
      if filter_by_visibility:
         workouts = workouts.filter(public=filter_by_visibility)

      filter_by_bodyweight = request.GET.get('filter_by_bodyweight', '')
      if filter_by_bodyweight.isnumeric():
         # For integer values, will be displayed results with floats number but integer part equal to filtered value
         if filter_by_bodyweight.isdigit():
            workouts = workouts.filter(bodyweight__icontains=int(filter_by_bodyweight))
         else:
            workouts = workouts.filter(bodyweight=filter_by_bodyweight)

      
      workouts_count = workouts.count()
   else:
      workouts = []

   context = {
      'workouts': workouts,
      'workouts_count': workouts_count,
   }

   return render(request, 'backend/workouts.html', context)


@login_required(login_url='login')
def view_workout(request, workout_id):
   """View used by user to see a specific workout, own one or a public one"""
   workout = get_object_or_404(Workout, pk=workout_id)
   workingsets = WorkingSet.objects.filter(user=request.user).order_by('id')

   context = {
      'workout': workout,
      'workingsets': workingsets
   }
   return render(request, 'backend/view_workout.html', context)


@login_required(login_url='login')
def create_workout(request):
   """View used to create a workout"""
   # Import cookie from workout_day_endpoint to use same target_data as the workout shown in homepage.
   target_date = request.COOKIES.get('targetDate', date.today())
   existing_workout = Workout.objects.filter(Q(user=request.user) & Q(created=target_date))
   
   if existing_workout:
      return HttpResponse('You already have a workout created for today. Delete it before creating another.')
   
   if request.method == "POST":
      form = WorkoutForm(request.POST)
      if form.is_valid():
         workout = form.save(commit=False)
         workout.user = request.user
         workout.created = target_date
         workout.save()
         # return redirect('home')
         return redirect(build_redirect_url(request, default_url=''))
   else:
      form = WorkoutForm()

   context = {
      'form': form
   }
   return render(request, 'backend/create_workout.html', context)


@login_required(login_url='login')
def import_workout(request, workout_id):
   """View used to import workout (owned by user or public ones)"""
   
   target_date = request.COOKIES.get('targetDate', date.today())
   existing_workout = Workout.objects.filter(Q(user=request.user) & Q(created=target_date))

   if existing_workout:
      return HttpResponse('You already have a workout created for today. Delete it before importing.')

   imported_workout = Workout.objects.get(pk=workout_id)

   # Create new workout for current user based by imported one
   new_workout = Workout(
      user=request.user,
      name=imported_workout.name,
      created=target_date,
   )
   new_workout.save()

   for order, imported_exercise in enumerate(imported_workout.exercises.all(), start=1):
      # Check if the user already has a muscle group with the same name as the one being in imported workout
      user_musclegroup = MuscleGroup.objects.filter(user=request.user, name=imported_exercise.musclegroup.name).first()

      # If the muscle group doesn't exist, create it for the current user
      if not user_musclegroup:
         user_musclegroup = MuscleGroup(
               user=request.user,
               name=imported_exercise.musclegroup.name,
               created=date.today(),
         )
         user_musclegroup.save()

      # Check if the exercise already exists for the current user in the specified muscle group
      existing_exercise = Exercise.objects.filter(user=request.user, name=imported_exercise.name, musclegroup=user_musclegroup).first()

      # If the exercise doesn't exist, create it for the current user
      if not existing_exercise:
         new_exercise = Exercise(
               user=request.user,
               name=imported_exercise.name,
               musclegroup=user_musclegroup,
               created=target_date,
         )
         new_exercise.save()

      # Add the exercise to the new workout with the specified order
      new_workout_exercise = WorkoutExercise(
         workout=new_workout,
         exercise=existing_exercise if existing_exercise else new_exercise,
         order=order,
      )
      new_workout_exercise.save()

   # return redirect('home')
   return redirect(build_redirect_url(request, default_url=''))


from django.http import QueryDict

@login_required(login_url='login')
def edit_workout(request, workout_id):
   """View used to edit fields from existing workout"""
   workout = Workout.objects.get(pk=workout_id, user=request.user)
   form = WorkoutForm(instance=workout)

   if request.method == "POST":
      form = WorkoutForm(request.POST, instance=workout)
      if form.is_valid():
         form.save()
         # return redirect('home')
         return redirect(build_redirect_url(request, default_url=''))
      
   context = {
      'form': form
   }
   return render(request, 'backend/create_workout.html', context)


@login_required(login_url='login')
def delete_workout(request, workout_id):
   """View used to delete existing workout"""
   workout = get_object_or_404(Workout, pk=workout_id, user=request.user)

   if request.method == "POST":
      workout.delete()
      # return redirect('home')
      return redirect(build_redirect_url(request, default_url=''))
   
   context = {
      'workout': workout
   }
   return render(request, 'backend/delete_workout.html', context)


@login_required(login_url='login')
def add_exercise(request, workout_id):
   """View used to display all exercises with their muscle groups, with option of search exercise by name or muscle group"""
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
      'workout': workout,
   }
   return render(request, 'backend/add_exercise.html', context)


@login_required(login_url='login')
def add_exercise_to_workout(request, exercise_id, workout_id):
   """View to manage adding a specific exercise to a specific workout"""
   workout = Workout.objects.get(pk=workout_id)
   exercise = Exercise.objects.get(pk=exercise_id)

   # Exercises order in workout according to the order of their addition by the user
   order = workout.exercises.count() + 1

   # Add exercise to workout with their order using WorkoutExercise model created for this
   workout_exercise = WorkoutExercise.objects.create(workout=workout, exercise=exercise, order=order)
   
   # return redirect('home')
   return redirect(build_redirect_url(request, default_url=''))


@login_required(login_url='login')
def delete_exercise_from_workout(request, exercise_id):
   """View used to to remove exercise from workout"""
   exercise = get_object_or_404(Exercise, pk=exercise_id, user=request.user)

   

   if request.method == "POST":
      workouts_with_exercise = Workout.objects.filter(exercises=exercise, user=request.user)

      # Work with the first workout with this exercise
      if workouts_with_exercise.exists():
         workout = workouts_with_exercise.first()

         # Delete associated working sets for the exercise remove
         working_sets_to_delete = WorkingSet.objects.filter(exercise=exercise, user=request.user)
         working_sets_to_delete.delete()

         # Remove exercise from the workout
         workout.exercises.remove(exercise)
         # return redirect('home')
         return redirect(build_redirect_url(request, default_url=''))
   
   context = {
      'exercise': exercise
   }
   return render(request, 'backend/delete_exercise_from_workout.html', context)


@login_required(login_url='login')
def add_workingset_to_exercise(request, exercise_id, workout_id):
   """View used to add working set to exercise existing in a workout"""
   exercise = Exercise.objects.get(pk=exercise_id, user=request.user)
   workout = Workout.objects.get(pk=workout_id, user=request.user)

   
   target_date = request.COOKIES.get('targetDate', date.today())

   if request.method == "POST":
      repetitions = request.POST.get('repetitions')
      weight = request.POST.get('weight')
      distance = request.POST.get('distance')
      time = request.POST.get('time')

      new_set = WorkingSet.objects.create(
         user=request.user,
         workout=workout,
         exercise=exercise,
         repetitions=repetitions if repetitions else None,
         weight=weight if weight else None,
         distance=distance if distance else None,
         time=time if time else None,
         created=target_date,
      )

      # return redirect('home')
      return redirect(build_redirect_url(request, default_url=''))

   context = {
      'exercise': exercise,
      'workout': workout,
   }
   return render(request, 'backend/add_workingset_to_exercise.html', context)


@login_required(login_url='login')
def delete_workingset_from_exercise(request, workingset_id):
   """View used to delete working set from exercise existing in a workout"""
   workingset = get_object_or_404(WorkingSet, pk=workingset_id, user=request.user)


   if request.method == "POST":
         workingset.delete()
         # return redirect('home')
         return redirect(build_redirect_url(request, default_url=''))

   context = {
      'workingset': workingset
   }
   return render(request, 'backend/delete_workingset_from_exercise.html', context)


@login_required(login_url='login')
def edit_workingset(request, workingset_id):
   """View used to edit values of existing workingset"""
   workingset = WorkingSet.objects.get(pk=workingset_id, user=request.user)

   # Removes fields with value None from the form field list so form will display only fields with completed values by user
   fields_to_exclude = []
   for field in ['weight', 'repetitions', 'distance', 'time']:
      if getattr(workingset, field) is None:
         fields_to_exclude.append(field)

   # Define a Meta class for the current form with excluded fields
   class CustomMeta_WorkingSet:
      model = WorkingSet
      fields = [field for field in ['weight', 'repetitions', 'distance', 'time'] if field not in fields_to_exclude]

   # Create a dynamic form class: 1st arg - new name class; 2nd arg - tuple with parent class; 3rd arg - dict with new values
   CustomForm_WorkingSet = type('CustomWorkingSetForm', (WorkingSetForm,), {'Meta': CustomMeta_WorkingSet})

   form = CustomForm_WorkingSet(instance=workingset)

   if request.method == "POST":
      form = CustomForm_WorkingSet(request.POST, instance=workingset)
      if form.is_valid():
         form.save()
         # return redirect('home')
         return redirect(build_redirect_url(request, default_url=''))

   context = {
      'form': form
   }
   return render(request, 'backend/create_workingset.html', context)


@login_required(login_url='login')
def musclegroups(request):
   """View used by user to see all muscle groups"""
   musclegroups = MuscleGroup.objects.filter(user=request.user)
   musclegroups_count = musclegroups.count()

   context = {
      'musclegroups': musclegroups,
      'musclegroups_count': musclegroups_count
   }
   return render(request, 'backend/musclegroups.html', context)


@login_required(login_url='login')
def create_musclegroup(request):
   """View used by user to add a muscle group"""
   if request.method == "POST":
      form = MuscleGroupForm(request.POST)
      if form.is_valid():
         musclegroup = form.save(commit=False)
         musclegroup.user = request.user
         musclegroup.save()
         # return redirect('home')
         return redirect(build_redirect_url(request, default_url=''))
   else:
      form = MuscleGroupForm()
   context = {
      'form': form
   }
   return render(request, 'backend/create_musclegroup.html', context)


@login_required(login_url='login')
def delete_musclegroup(request, musclegroup_id):
   """View used by user to delete muscle group"""
   musclegroup = get_object_or_404(MuscleGroup, pk=musclegroup_id, user=request.user)

   if request.method == "POST":
      musclegroup.delete()
      return redirect('musclegroups')

   context = {
      'musclegroup': musclegroup
   }
   return render(request, 'backend/delete_musclegroup.html', context)


@login_required(login_url='login')
def exercises(request):
   """View used by user to see all his exercises, and search them by their name or by their muscle group"""
   exercises = Exercise.objects.filter(user=request.user)
   exercises_count = exercises.count()

   if request.user.is_authenticated:
      q = request.GET.get('q', '')
      exercises = Exercise.objects.filter(
         Q(musclegroup__name__icontains = q) |
         Q(name__icontains = q),
         user=request.user
      )
      exercises_count = exercises.count()
   else:
      exercises = []

   context = {
      'exercises': exercises,
      'exercises_count': exercises_count
   }
   return render(request, 'backend/exercises.html', context)


@login_required(login_url='login')
def create_exercise(request):
   """View used to create exercise"""
   if request.method == "POST":
      form = ExerciseForm(request.user, request.POST)
      if form.is_valid():
         exercise = form.save(commit=False)
         exercise.user = request.user
         exercise.save()
         return redirect('exercises')
   else:
      form = ExerciseForm(request.user)

   context = {
      'form': form
   }
   return render(request, 'backend/create_exercise.html', context)


@login_required(login_url='login')
def delete_exercise(request, exercise_id):
   """View used to delete exercise"""
   exercise = get_object_or_404(Exercise, pk=exercise_id, user=request.user)

   if request.method == "POST":
      exercise.delete()
      return redirect('exercises')

   context = {
      'exercise': exercise
   }
   return render(request, 'backend/delete_exercise.html', context)


@login_required(login_url='login')
def bodyweight_analysis(request):
   """View used to see a bodyweight analyze"""
   workouts = Workout.objects.filter(user=request.user)

   context = {
      'workouts': workouts
   }

   return render(request, 'backend/bodyweight_analysis.html', context)


@login_required(login_url='login')
def exercise_analysis(request):
   """View used to see a each exercise anaylize"""
   exercises = Exercise.objects.filter(user=request.user)
   workingsets = WorkingSet.objects.filter(user=request.user)

   context = {
      'exercises': exercises,
      'workingsets': workingsets
   }

   return render(request, 'backend/exercise_analysis.html', context)


@login_required(login_url='login')
def exercise_records(request):
   """View used to see a each exercise record based by his working set records"""
   exercises = Exercise.objects.all()
   workingsets = WorkingSet.objects.all()

   context = {
      'exercises': exercises,
      'workingsets': workingsets,
   }

   return render(request, 'backend/exercise_records.html', context)


@login_required(login_url='login')
def public_workouts(request):
   """View used by user to see all public workouts (workouts of other users)"""
   public_workouts = Workout.objects.filter(public="yes")

   context = {
      'public_workouts': public_workouts,
   }
   return render(request, 'backend/public_workouts.html', context)


def about_help(request):


   context = {

   }
   return render(request, 'backend/about_help.html', context)


def build_redirect_url(request, default_url=''):
   """Created for refactoring: used to redirect users, after an action, to the same page from which they initiated the action"""
   days_diff = request.COOKIES.get('daysDiff')

   if days_diff is not None:
      return f'{default_url}/?days_diff={days_diff}'
   else:
      return default_url