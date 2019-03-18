from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
import numpy as np
from django.db.models import Avg
# Create your models here.

class Profile(models.Model):
    profile_photo = models.ImageField(upload_to ='prof_pictures/')
    bio = HTMLField()
    phone = models.IntegerField(default=0) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def save_profile(self):
        self.save()
    
    def delete_profile(self):
        self.delete()
    
    @classmethod
    def get_profile(cls,id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls,id):
        profile = Profile.objects.filter(user=id).first()
        return profile

class Project(models.Model):
    photo = models.ImageField(upload_to ='prof_pictures/')
    project_name = models.CharField(max_length = 100)
    project_caption =  models.CharField(max_length = 100)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', default="")

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def search_project(cls,search_term):
        projects = cls.objects.filter(project_name__icontains=search_term)
        return projects

    @classmethod
    def get_project(cls, id):
        project = Project.objects.get(pk=id)
        return project
    
    @classmethod
    def get_images(cls):
        projects = Project.objects.all()
        return projects

    @classmethod
    def get_profile_image(cls,profile):
        projects = Project.objects.filter(user_profile__pk=profile)
        return projects

    def design_rating(self):
        all_designs =list( map(lambda x: x.design, self.reviews.all()))
        return np.mean(all_designs)

    def usability_rating(self):
        all_usability =list( map(lambda x: x.usability, self.reviews.all()))
        return np.mean(all_usability)

    def content_rating(self):
        all_content =list( map(lambda x: x.content, self.reviews.all()))
        return np.mean(all_content)

class Reviews(models.Model):
    RATING = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    comment = HTMLField()
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='reviews',null=True)
    design = models.IntegerField(choices=RATING,default=0)
    usability = models.IntegerField(choices=RATING,default=0)
    content = models.IntegerField(choices=RATING,default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def save_review(self):
        self.save()

    @classmethod
    def get_reviews(cls,id):
        reviews = Reviews.objects.filter(project_id = id)
        return reviews

    @classmethod
    def get_average(cls):
        usability = Reviews.objects.all().aggregate(Avg('usability'))
        return usability
    
