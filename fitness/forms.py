# Django
from django import forms
from django.forms import ModelForm

# App
from fitness.models import MuscleGroup, Exercise, Workout, WorkingSet, WorkoutComment


class MuscleGroupForm(ModelForm):
    """Form used when create / edit muscle group"""
    class Meta:
        model = MuscleGroup
        fields = ['name']


class ExerciseForm(ModelForm):
    """Form used when create / edit exercise"""
    def __init__(self, user, *args, **kwargs):
        """Filter the muscle group options for the current user"""
        super(ExerciseForm, self).__init__(*args, **kwargs)
        self.fields['musclegroup'].queryset = MuscleGroup.objects.filter(user=user)
        # Use only the muscle group's self.name, not his full database name
        self.fields['musclegroup'].label_from_instance = lambda obj: obj.name
    
    class Meta:
        model = Exercise
        fields = ['name', 'musclegroup']


class WorkoutForm(ModelForm):
    """Form used when create / edit workout"""
    class Meta:
        model = Workout
        fields = ['name', 'bodyweight', 'note', 'public']


class WorkingSetForm(forms.ModelForm):
    """Form used when create / edit working set"""
    def __init__(self, *args, **kwargs):
        # Exclude fields with None values only when editing
        super(WorkingSetForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            fields_to_exclude = [field for field in self.fields if getattr(self.instance, field) is None]
            for field in fields_to_exclude:
                self.fields.pop(field)
    
    class Meta:
        model = WorkingSet
        fields = ['type', 'weight', 'repetitions', 'distance', 'time']


class WorkoutCommentForm(ModelForm):
    """Form used when edit a self comment from a public workout"""
    class Meta:
        model = WorkoutComment
        fields = ['content']