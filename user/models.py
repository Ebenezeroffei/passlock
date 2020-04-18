from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class ProfilePic(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    profile = models.ImageField(default = 'default_user.png',upload_to = 'profile_pics')
    
    def __str__(self):
        return f"{self.user.username}'s profile pic"
    
    def save(self):
        super().save()
        img = Image.open(self.profile.path)
        if img.height > 200 or img.width > 200:
            output_size  =(200,200)
            img.thumbnail(output_size)
            img.save(self.profile.path)