from django import forms
from django.forms import ModelForm
from .models import MuscleGroup, Exercise, WorkingSet, Workout


class WorkoutForm(ModelForm):
    """Form used when create / edit workout"""
    class Meta:
        model = Workout
        fields = ['name', 'bodyweight', 'public', 'note']


class WorkingSetForm(ModelForm):
    """Form used when create / edit working set"""
    class Meta:
        model = WorkingSet
        fields = ['weight', 'repetitions', 'distance', 'time']


class MuscleGroupForm(ModelForm):
    """Form used when create muscle group"""
    class Meta:
        model = MuscleGroup
        fields = ['name']


class ExerciseForm(ModelForm):
    """Form used when create exercise"""
    
    def __init__(self, user, *args, **kwargs):
        """Filter the muscle group options for the current user"""
        super(ExerciseForm, self).__init__(*args, **kwargs)
        self.fields['musclegroup'].queryset = MuscleGroup.objects.filter(user=user)
    
    class Meta:
        model = Exercise
        fields = ['name', 'musclegroup']