from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Project, Reviews

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
