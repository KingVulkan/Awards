from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile,Project,Reviews

# Create your tests here.
class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='a')
        self.new_project = Project(project_name='Food', project_caption='Delicious', user_profile=self.user)
        

    def test_instance(self):
        self.assertTrue(isinstance(self.new_project,Project))

    def test_save_project(self):
        self.new_project.save()
        projects = Project.objects.all()
        self.assertTrue(len(projects)>0)

    def test_get_project(self):
        self.new_project.save()
        project = Project.get_project(1)
        self.assertTrue(project==self.new_project)

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id =1,username='a')
        self.new_profile = Profile(user=self.user, bio='I am awesome', phone=1112222)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))

    def test_get_profile(self):
        self.new_profile.save()
        profile = Profile.get_profile(1)
        self.assertTrue(profile== self.new_profile)

    
    def test_filter_by_id(self):
        self.new_profile.save()
        profile = Profile.filter_by_id(1)
        self.assertTrue(profile== self.new_profile)
