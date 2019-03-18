from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProjectForm, ReviewForm, ProfileForm
from .models import Profile,Project,Reviews

# Create your views here.
 
def home(request):
    images = Project.get_images()
    

    return render(request, 'home.html', {'images':images})
    
def register(request):
    if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                redirect('login.html')
    else:
        form=RegistrationForm()
        return render(request, 'registration/registration_form.html', {'form':form})


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

@login_required(login_url='/accounts/login')
def project_review(request, project_id):
    project = Project.get_project(project_id)
    
    reviews = Reviews.get_reviews(project_id)
   
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            review = form.save(commit=False)
            review.project = project
            review.user = request.user
            review.design = design
            review.usability = usability
            review.content = content
            review.save()
            return redirect('project_review', project_id=project_id)
    else:
        form = ReviewForm()
        return render(request,'review.html',{'project':project ,'form':form, 'reviews':reviews})
