from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Project, Reviews

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text = 'Required')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


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
