from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserRegistrationForm(UserCreationForm):
    """Form used to add email field on sign up page"""
    email = forms.EmailField(required=True)
    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AccountRecoveryForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account is associated with this email.")
        return email