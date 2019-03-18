from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProjectForm, ReviewForm, ProfileForm
from .models import Profile,Project,Reviews
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import ProfileSerializer, ProjectSerializer
from .permissions import IsAdminOrReadOnly

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

@login_required(login_url='/accounts/login')
def edit_profile(request):
   
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile', username=request.user)
            
    else:
        form = ProfileForm()

    return render(request, 'profile/editprofile.html', {'form':form, 'profile':profile})

def search_project(request):
    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        found_project = Project.search_project(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{'message':message, 'projects':found_project})
    else:
        message = 'Enter term to search'
        return render(request, 'search.html', {'message':message})

class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
