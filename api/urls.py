from django.urls import path
from . import views

urlpatterns = [
    # path('', views, name=''),
    path('workouts/', views.get_workouts, name='get_workouts'),
    path('workout_exercises/', views.get_workout_exercises, name='get_workout_exercises'),
    path('musclegroups/', views.get_musclegroup, name='get_musclegroup'),
    path('exercises/', views.get_exercises, name='get_exercises'),
    path('workingsets/', views.get_workingsets, name='get_workingsets'),
    # path('add/', views.add_workout),
]

