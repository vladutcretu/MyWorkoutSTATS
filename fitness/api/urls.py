# Django & DRF
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# App
from . import views


router = DefaultRouter()
router.register(r'musclegroups', views.MuscleGroupAPIView, basename='musclegroups')
router.register(r'exercises', views.ExerciseAPIView, basename='exercises')
router.register(r'workouts', views.WorkoutAPIView, basename='workouts')
router.register(r'workout-exercises', views.WorkoutExerciseAPIView, basename='workout-exercises')
router.register(r'sets', views.WorkingSetAPIView, basename='sets')
router.register(r'workouts-detailed', views.DetailedWorkoutAPIView, basename='workouts-detailed')


urlpatterns = [
    path('', include(router.urls))
]