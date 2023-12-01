# users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'wallet', 'full_name', 'date_of_birth', 'phone_number', 'identification_type', 'id_front_image', 'id_back_image', 'selfie_with_id_image', 'social_security_number']


class AdminNotificationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
