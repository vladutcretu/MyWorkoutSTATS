from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms import ModelForm

from .models import CustomUser, MuscleGroup, Exercise, Workout, WorkingSet


class CustomUserRegistrationForm(UserCreationForm):
    """Form used to add email field on sign up page"""
    email = forms.EmailField(required=True)
    usable_password = None

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class AccountRecoveryForm(forms.Form):
    """Form used for account recovery using email address"""
    email = forms.EmailField(label="Email", max_length=254, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("No account is associated with this email.")
        return email
    

class EditProfileForm(forms.ModelForm):
    """Form used to edit a user profile"""
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'first_name', 'last_name', 'age', 'city', 'bio', 'instagram_url']


class ChangePasswordForm(SetPasswordForm):
    """Form used by user to change his account password"""
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']


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
        fields = ['name', 'bodyweight', 'public', 'note']


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
        fields = ['weight', 'repetitions', 'distance', 'time']