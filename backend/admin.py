from django.contrib import admin
from .models import CustomUser, MuscleGroup, Exercise


admin.site.register(CustomUser)
admin.site.register(MuscleGroup)
admin.site.register(Exercise)
