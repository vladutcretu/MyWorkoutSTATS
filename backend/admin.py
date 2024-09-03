from django.contrib import admin
from .models import CustomUser, MuscleGroup, Exercise, Workout, WorkoutExercise


admin.site.register(CustomUser)
admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(WorkoutExercise)
