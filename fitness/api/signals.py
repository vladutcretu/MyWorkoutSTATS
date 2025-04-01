# Django
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

# App
from fitness.models import (
    MuscleGroup,
    Exercise,
    Workout,
    WorkoutExercise,
    WorkingSet,
)


@receiver([post_save, post_delete], sender=MuscleGroup)
def invalidate_musclegroup_cache(sender, instance, **kwargs):
    """
    Invalidate musclegroup list / retrieve caches when a musclegroup is
    created, updated or deleted
    """

    cache.delete_pattern("*MuscleGroupAPIView*")


@receiver([post_save, post_delete], sender=Exercise)
def invalidate_exercise_cache(sender, instance, **kwargs):
    """
    Invalidate exercise list / retrieve caches when an exercise is
    created, updated or deleted
    """

    cache.delete_pattern("*ExerciseAPIView*")
    cache.delete_pattern("*DetailedWorkoutAPIView*")


@receiver([post_save, post_delete], sender=Workout)
def invalidate_workout_cache(sender, instance, **kwargs):
    """
    Invalidate workout list / retrieve caches when a workout is
    created, updated or deleted
    """

    cache.delete_pattern("*WorkoutAPIView*")
    cache.delete_pattern("*DetailedWorkoutAPIView*")


@receiver([post_save, post_delete], sender=WorkoutExercise)
def invalidate_workout_exercise_cache(sender, instance, **kwargs):
    """
    Invalidate workout_exercise list / retrieve caches when a workout_exercise
    is created, updated or deleted
    """

    cache.delete_pattern("*WorkoutExerciseAPIView*")
    cache.delete_pattern("*DetailedWorkoutAPIView*")


@receiver([post_save, post_delete], sender=WorkingSet)
def invalidate_workingset_cache(sender, instance, **kwargs):
    """
    Invalidate workingset list / retrieve caches when a workingset is
    created, updated or deleted
    """

    cache.delete_pattern("*WorkingSetAPIView*")
    cache.delete_pattern("*DetailedWorkoutAPIView*")
