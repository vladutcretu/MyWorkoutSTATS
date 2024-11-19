# Django
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

# App
from fitness.models import Workout, WorkingSet


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
   response = render(request, 'main.html', context)
   response.set_cookie('daysDiff', days_diff)
   response.set_cookie('targetDate', str(target_date))
   return response


def build_redirect_url(request, default_url=''):
   """Created for refactoring: after an action redirect users to the same page from which they initiated the action"""
   days_diff = request.COOKIES.get('daysDiff')

   if days_diff is not None:
      return f'{default_url}/?days_diff={days_diff}'
   else:
      return default_url