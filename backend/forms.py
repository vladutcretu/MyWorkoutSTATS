from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms import ModelForm

from .models import CustomUser, MuscleGroup, Exercise


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
        # Use only the muscle group's self.name, not his full database name
        self.fields['musclegroup'].label_from_instance = lambda obj: obj.name
    
    class Meta:
        model = Exercise
        fields = ['name', 'musclegroup']