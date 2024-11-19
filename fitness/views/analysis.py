# Django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# App
from fitness.models import Workout, WorkingSet, Exercise


@login_required(login_url='login')
def analysis_bodyweight(request):
   """View used by user to see his bodyweight analysis"""
   workouts = Workout.objects.filter(user=request.user)

   context = {
      'workouts': workouts
   }

   return render(request, 'analysis/bodyweight.html', context)


@login_required(login_url='login')
def analysis_volume(request):
   """View used by user to see the volume analysis for a selected exercise"""
   exercises = Exercise.objects.filter(user=request.user)

   context = {
      'exercises': exercises
   }

   return render(request, 'analysis/volume.html', context)


@login_required(login_url='login')
def get_volume_data(request):
   """Ajax view to return the volume data for a specific (target) exercise"""
   exercise_id = request.GET.get('exercise_id')

   workingsets = WorkingSet.objects.filter(user=request.user, exercise_id=exercise_id)

   # Group sets by days and calculate the total volume (weight * repetitions)
   volume_data = {}
   for workingset in workingsets:
      date_str = workingset.created.strftime('%Y-%m-%d')  # Group all sets from specific day
      volume = workingset.weight * workingset.repetitions
      if date_str in volume_data:
         volume_data[date_str] += volume
      else:
         volume_data[date_str] = volume

   # Return chronologically ordered data
   sorted_volume_data = sorted(volume_data.items())  # List tuple(data, volume)
   data = {
      'dates': [item[0] for item in sorted_volume_data],
      'volumes': [item[1] for item in sorted_volume_data]
   }

   return JsonResponse(data)


@login_required(login_url='login')
def analysis_records(request):
   """View used by user to see each exercise record, based by his sets logged"""
   exercises = Exercise.objects.filter(user=request.user)
   workingsets = WorkingSet.objects.filter(user=request.user)

   context = {
      'exercises': exercises,
      'workingsets': workingsets
   }

   return render(request, 'analysis/records.html', context)


@login_required(login_url='login')
def get_record_data(request):
   """Ajax view to return the highest set based on set type and exercise"""
   exercise_id = request.GET.get('exercise_id')
   record_type = request.GET.get('record_type')

   workingsets = WorkingSet.objects.filter(user=request.user, exercise_id=exercise_id)

   if record_type == "weight" and workingsets:
      record_set = workingsets.order_by('-weight').first()  # Biggest weight
      if not record_set.weight and not record_set.repetitions:
         record_set = None
   elif record_type == "repetitions" and workingsets:
      record_set = workingsets.order_by('-repetitions').first()  # Most reps
      if not record_set.weight and not record_set.repetitions:
         record_set = None
   elif record_type == "distance" and workingsets:
      record_set = workingsets.order_by('-distance').first()  # Longest distance
      if not record_set.distance and not record_set.time:
         record_set = None
   elif record_type == "time" and workingsets:
      record_set = workingsets.order_by('-time').first()  # Highest time
      if not record_set.distance and not record_set.time:
         record_set = None
   else:
         record_set = None

   if record_set:
      data = {
         'exercise': record_set.exercise.name,
         'type': record_set.type,
         'weight': record_set.weight,
         'reps': record_set.repetitions,
         'distance': record_set.distance,
         'time': record_set.time,
         'date': record_set.created.strftime('%b. %d, %Y'),
      }
   else:
      data = {'error': 'No record found.'}

   return JsonResponse(data)