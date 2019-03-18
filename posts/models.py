from django.db import models

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

