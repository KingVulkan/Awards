from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProjectForm, ReviewForm, ProfileForm
from .models import Profile,Project,Reviews

# Create your views here.

def profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_info = Profile.get_profile(profile.id)
    except:
        profile_info = Profile.filter_by_id(profile.id)
    projects = Project.get_profile_image(profile.id)
    title = f'@{profile.username}'
    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_info':profile_info, 'projects':projects})  

@login_required(login_url='/accounts/login')
def project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user_profile = request.user
            upload.save()
            return redirect('profile', username=request.user)
    else:
        form = ProjectForm()

    return render(request, 'profile/uploadproject.html', {'form':form})
