from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Project, Reviews

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
       
        exclude = ['user_profile']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude = ['user','project','user_rating']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
