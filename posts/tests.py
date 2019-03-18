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


