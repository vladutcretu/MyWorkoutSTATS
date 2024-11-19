# django
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

# App
from core.models import CustomUser


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