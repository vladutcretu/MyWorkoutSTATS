from django.contrib import admin

# Register your models here.

from .models import MuscleGroup, Exercise, WorkingSet, Workout, WorkoutExercise
admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(WorkingSet)
admin.site.register(Workout)
admin.site.register(WorkoutExercise)