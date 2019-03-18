from rest_framework import serializers
from .models import Project, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ( 'user', 'profile_photo', 'bio','phone')
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ( 'project_name','user_profile','project_caption')