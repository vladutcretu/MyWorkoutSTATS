from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse

from datetime import date, timedelta
from django.utils import timezone

from .models import CustomUser, MuscleGroup, Exercise, Workout, WorkoutExercise, WorkingSet, WorkoutComment
from .forms import CustomUserRegistrationForm, AccountRecoveryForm, EditProfileForm, ChangePasswordForm
from .forms import MuscleGroupForm, ExerciseForm, WorkoutForm, WorkingSetForm, WorkoutCommentForm


def main(request):
   """View used to display in main page the correct workout based by user actions"""
   # Obtain days_diff value from query string
   days_diff = int(request.GET.get('days_diff', 0))

   # Calculate the date for the desired day based on days_diff value (output is YYYY-MM-DD)
   target_date = timezone.now().date() + timedelta(days=days_diff)

   # If user logged in, get only the workout they want on the page
   if request.user.is_authenticated:
      workouts = Workout.objects.filter(user=request.user, created=target_date)
      workingsets = WorkingSet.objects.filter(user=request.user, created=target_date)
   # If user not logged in, workout is None so we'll display only basic info on page
   else:
      workouts, workingsets = [], []

   context = {
      'days_diff': days_diff,
      'target_date': target_date,
      'workouts': workouts,
      'workingsets': workingsets
   }

   # Add days_diff & target_date in cookies to use it in other pages
   response = render(request, 'backend/main.html', context)
   response.set_cookie('daysDiff', days_diff)
   response.set_cookie('targetDate', str(target_date))
   return response



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Auth VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def user_login(request):
   """View for Log In page"""
   if request.user.is_authenticated:
      return redirect('main')
   
   if request.method == 'POST':
      username = request.POST.get('username').lower()
      password = request.POST.get('password')

      try: 
         user = CustomUser.objects.get(username=username)
      except:
         messages.error(request, "User does not exist")

      user = authenticate(request, username=username, password=password)

      if user is not None:
         login(request, user)
         return redirect('main')
      else:
         messages.error(request, "Password is incorrect")

   return render(request, 'backend/user_login.html')


def user_logout(request):
   """View for Log out page"""
   logout(request)
   return redirect('main')


def user_signup(request):
   """View for Sign Up page""" 
   if request.user.is_authenticated:
      return redirect('main')

   form = CustomUserRegistrationForm()

   if request.method == 'POST':
      form = CustomUserRegistrationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('main')
      else:
         messages.error(request, "Something bad happened. Try again please!")

   context = {
      'form': form
   }
   return render (request, 'backend/user_signup.html', context)


def user_account_recovery(request):
   if request.user.is_authenticated:
      return redirect('main')
   
   form = AccountRecoveryForm()
   
   if request.method == 'POST':
      form = AccountRecoveryForm(request.POST)
      if form.is_valid():
         # Instructions to send recovery email here # 
         messages.success(request, 'An email has been sent to your email address with further instructions. Please check it!')
   else:
      form = AccountRecoveryForm()
   
   context = {
      'form' : form
   }
   return render(request, 'backend/user_recover.html', context)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Profile VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@login_required(login_url='login')
def user_profile(request, user_id):
   """View for User Profile page"""
   user = CustomUser.objects.get(pk=user_id)
   public_workouts = Workout.objects.filter(user=user_id, public="yes")

   context = {
      'user': user,
      'public_workouts': public_workouts
   }
   return render(request, 'backend/user_profile.html', context)


@login_required(login_url='login')
def user_profile_edit(request):
   """View to edit user profile informations"""
   if request.method == 'POST':
      form = EditProfileForm(request.POST, request.FILES, instance=request.user)
      if form.is_valid():
         form.save()
         return redirect('profile', user_id=request.user.id)
   else:
      form = EditProfileForm(instance=request.user)
   
   context = {
      'form': form
   }
   return render(request, 'backend/user_profile_edit.html', context)


@login_required(login_url='login')
def user_change_password(request):
   """View for Change Password page""" 
   if request.method == 'POST':
      form = ChangePasswordForm(request.user, request.POST)
      if form.is_valid():
         user = form.save()
         update_session_auth_hash(request, user)
         messages.success(request, "Your password has been changed.")
      else:
         for error in list(form.errors.values()):
            messages.error(request, error)
   else:
      form = ChangePasswordForm(request.user)

   context = {
      'form': form
   }
   return render (request, 'backend/user_change_password.html', context)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # MuscleGroups VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@login_required(login_url='login')
def view_musclegroups(request):
   """View used by user to see all muscle groups"""
   musclegroups = MuscleGroup.objects.filter(user=request.user)
   musclegroups_count = musclegroups.count()

   context = {
      'musclegroups': musclegroups,
      'musclegroups_count': musclegroups_count
   }
   return render(request, 'backend/musclegroups_view.html', context)


@login_required(login_url='login')
def create_musclegroups(request):
   """View used by user to add a muscle group"""
   if request.method == "POST":
      form = MuscleGroupForm(request.POST)
      if form.is_valid():
         musclegroup = form.save(commit=False)
         musclegroup.user = request.user
         musclegroup.save()
         return redirect('musclegroups')
   else:
      form = MuscleGroupForm()

   context = {
      'form': form
   }
   return render(request, 'backend/musclegroups_create.html', context)


@login_required(login_url='login')
def edit_musclegroups(request, musclegroup_id):
   """View used to edit fields from existing muscle group"""
   musclegroup = get_object_or_404(MuscleGroup, pk=musclegroup_id, user=request.user)
   form = MuscleGroupForm(instance=musclegroup)

   if request.method == "POST":
      form = MuscleGroupForm(request.POST, instance=musclegroup)
      if form.is_valid():
         form.save()
         return redirect('musclegroups')
      
   context = {
      'form': form
   }
   return render(request, 'backend/musclegroups_create.html', context)


@login_required(login_url='login')
def delete_musclegroups(request, musclegroup_id):
   """View used by user to delete muscle group"""
   musclegroup = get_object_or_404(MuscleGroup, pk=musclegroup_id, user=request.user)

   if request.method == "POST":
      musclegroup.delete()
      return redirect('musclegroups')

   context = {
      'musclegroup': musclegroup
   }
   return render(request, 'backend/musclegroups_delete.html', context)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Exercises VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@login_required(login_url='login')
def view_exercises(request):
   """View used by user to see all exercises, and search them by their name"""
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
      'exercises_count': exercises_count,
   }
   return render(request, 'backend/exercises_view.html', context)


@login_required(login_url='login')
def create_exercises(request):
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
   return render(request, 'backend/exercises_create.html', context)


@login_required(login_url='login')
def edit_exercises(request, exercise_id):
   """View used to edit fields from existing muscle group"""
   exercise = get_object_or_404(Exercise, pk=exercise_id, user=request.user)
   form = ExerciseForm(instance=exercise, user=request.user)

   if request.method == "POST":
      form = ExerciseForm(request.user, request.POST, instance=exercise)
      if form.is_valid():
         form.save()
         return redirect('exercises')
      
   context = {
      'form': form
   }
   return render(request, 'backend/exercises_create.html', context)


@login_required(login_url='login')
def delete_exercises(request, exercise_id):
   """View used to delete exercise"""
   exercise = get_object_or_404(Exercise, pk=exercise_id, user=request.user)

   if request.method == "POST":
      exercise.delete()
      return redirect('exercises')

   context = {
      'exercise': exercise
   }
   return render(request, 'backend/exercises_delete.html', context)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Workouts VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@login_required(login_url='login')
def view_workouts(request):
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
         # For integer values will be displayed results with floats number but integer part equal to filtered value
         if filter_by_bodyweight.isdigit():
            workouts = workouts.filter(bodyweight__icontains=int(filter_by_bodyweight))
         else:
            workouts = workouts.filter(bodyweight=filter_by_bodyweight)

      workouts_count = workouts.count()
   else:
      workouts = []

   context = {
      'workouts': workouts,
      'workouts_count': workouts_count
   }

   return render(request, 'backend/workouts_view.html', context)


@login_required(login_url='login')
def create_workouts(request):
   """View used to create workout"""
   # Import cookie to use same target_data as the workout shown in main page (to create workout with the same date as date selected)
   target_date = request.COOKIES.get('targetDate', date.today())
   existing_workout = Workout.objects.filter(user=request.user, created=target_date)
   
   if existing_workout:
      return HttpResponse('You already have a workout created for this day. Delete it before creating another.')
   
   if request.method == "POST":
      form = WorkoutForm(request.POST)
      if form.is_valid():
         workout = form.save(commit=False)
         workout.user = request.user
         workout.created = target_date
         workout.save()
         return redirect(build_redirect_url(request, default_url=''))
   else:
      form = WorkoutForm()

   context = {
      'form': form
   }
   return render(request, 'backend/workouts_create.html', context)


@login_required(login_url='login')
def import_workouts(request, workout_id):
   """View used to import a workout (copy exercises and workingsets), owned by user or public one"""
   # Import cookie to use same target_data as the workout shown in main page (to create workout with the same date as date selected)
   target_date = request.COOKIES.get('targetDate', date.today())
   existing_workout = Workout.objects.filter(user=request.user, created=target_date).exists()

   if existing_workout:
      return HttpResponse('You already have a workout created for this day. Delete it before creating another.')

   # Get the workout to be imported
   imported_workout = get_object_or_404(Workout, pk=workout_id)

   # Create a new workout for user
   new_workout = Workout.objects.create(
      user=request.user,
      name=imported_workout.name,
      created=target_date
   )

   # Import exercises to workout
   for order, imported_exercise in enumerate(imported_workout.exercises.all(), start=1):
      # Create exercise or use existing one
      exercise = get_or_create_musclegroup_and_exercise(imported_exercise, request.user)

      # Add exercise to newly imported workout
      new_workout_exercise = WorkoutExercise.objects.create(
         workout=new_workout,
         exercise=exercise,
         order=order
      )

      # Import workingsets from imported exercise
      import_workingsets(imported_exercise, request.user, new_workout, exercise, target_date)

   return redirect(build_redirect_url(request, default_url=''))


@login_required(login_url='login')
def edit_workout(request, workout_id):
   """View used to edit fields from existing workout"""
   workout = Workout.objects.get(pk=workout_id, user=request.user)
   form = WorkoutForm(instance=workout)

   if request.method == "POST":
      form = WorkoutForm(request.POST, instance=workout)
      if form.is_valid():
         form.save()
         return redirect(build_redirect_url(request, default_url=''))
      
   context = {
      'form': form
   }
   return render(request, 'backend/workouts_create.html', context)


@login_required(login_url='login')
def delete_workout(request, workout_id):
   """View used to delete existing workout"""
   workout = get_object_or_404(Workout, pk=workout_id, user=request.user)

   if request.method == "POST":
      workout.delete()
      return redirect(build_redirect_url(request, default_url=''))
   
   context = {
      'workout': workout
   }
   return render(request, 'backend/workouts_delete.html', context)


@login_required(login_url='login')
def view_private_workout(request, workout_id):
   """View used by user to see a specific owned workout"""
   workout = get_object_or_404(Workout, pk=workout_id)
   workingsets = WorkingSet.objects.filter(user=request.user).order_by('id')

   context = {
      'workout': workout,
      'workingsets': workingsets
   }
   return render(request, 'backend/workouts_view_private.html', context)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Exercise to Workout VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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
   return render(request, 'backend/select_exercise.html', context)


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
   return render(request, 'backend/select_exercise_remove.html', context)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # WorkingSets VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@login_required(login_url='login')
def create_workingsets(request, exercise_id, workout_id):
   """View used to add working set to an existing exercise in a workout"""
   exercise = Exercise.objects.get(pk=exercise_id, user=request.user)
   workout = Workout.objects.get(pk=workout_id, user=request.user)

   target_date = request.COOKIES.get('targetDate', date.today())

   if request.method == "POST":
      type = request.POST.get('type', 'working')
      repetitions = request.POST.get('repetitions')
      weight = request.POST.get('weight')
      distance = request.POST.get('distance')
      time = request.POST.get('time')

      new_set = WorkingSet.objects.create(
         user=request.user,
         workout=workout,
         exercise=exercise,
         type = type,
         repetitions=repetitions if repetitions else None,
         weight=weight if weight else None,
         distance=distance if distance else None,
         time=time if time else None,
         created=target_date,
      )

      return redirect(build_redirect_url(request, default_url=''))

   context = {
      'exercise': exercise,
      'workout': workout
   }
   return render(request, 'backend/workingsets_create.html', context)


@login_required(login_url='login')
def edit_workingsets(request, workingset_id):
    """View used to edit values of existing working set"""
    workingset = get_object_or_404(WorkingSet, pk=workingset_id, user=request.user)
    form = WorkingSetForm(instance=workingset)

    if request.method == "POST":
        form = WorkingSetForm(request.POST, instance=workingset)
        if form.is_valid():
            form.save()
            return redirect(build_redirect_url(request, default_url=''))

    context = {
        'form': form
    }
    return render(request, 'backend/workingsets_edit.html', context)


@login_required(login_url='login')
def delete_workingsets(request, workingset_id):
   """View used to delete working set from an existing exercise in a workout"""
   workingset = get_object_or_404(WorkingSet, pk=workingset_id, user=request.user)

   if request.method == "POST":
         workingset.delete()
         return redirect(build_redirect_url(request, default_url=''))

   context = {
      'workingset': workingset
   }
   return render(request, 'backend/workingsets_delete.html', context)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Public Workouts VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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
   return render(request, 'backend/workouts_public.html', context)


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
   return render(request, 'backend/workouts_view_public.html', context)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Comment, Reply and Like to Public Workouts VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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
   return render(request, 'backend/comments_edit.html', context)


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
   return render(request, 'backend/comments_delete.html', context)


@login_required(login_url='login')
def like_workout(request, workout_id):
   """View for liking or unliking a workout"""
   workout = get_object_or_404(Workout, pk=workout_id)

   if request.user in workout.likes.all():
      workout.likes.remove(request.user)
   else:
      workout.likes.add(request.user)

   return redirect('view-public-workout', workout_id=workout.id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Refactoring VIEWS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def build_redirect_url(request, default_url=''):
   """Created for refactoring: after an action redirect users to the same page from which they initiated the action"""
   days_diff = request.COOKIES.get('daysDiff')

   if days_diff is not None:
      return f'{default_url}/?days_diff={days_diff}'
   else:
      return default_url
   

def get_or_create_musclegroup_and_exercise(imported_exercise, user):
   """Created for refactoring: get musclegroup and exercise from imported workout or create if user does not have it"""
   musclegroup, _ = MuscleGroup.objects.get_or_create(
      user=user,
      name=imported_exercise.musclegroup.name,
      defaults={'created': date.today()}
   )
   exercise, _ = Exercise.objects.get_or_create(
      user=user,
      name=imported_exercise.name,
      musclegroup=musclegroup,
      defaults={'created': date.today()}
   )
   return exercise


def import_workingsets(imported_exercise, user, workout, exercise, created):
   """Created for refactoring: creating (importing) workingsets of an exercise from an imported workout"""
   for imported_workingset in imported_exercise.workingsets.all():
      WorkingSet.objects.create(
         user=user,
         workout=workout,
         exercise=exercise,
         weight=imported_workingset.weight,
         repetitions=imported_workingset.repetitions,
         distance=imported_workingset.distance,
         time=imported_workingset.time,
         created=created
      )