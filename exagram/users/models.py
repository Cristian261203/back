from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True) 

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    bio = models.TextField(max_length=500, blank=True) 
    followers = models.ManyToManyField(User, related_name='profile_followers', blank=True)  
    following = models.ManyToManyField(User, related_name='profile_following', blank=True)  

    def __str__(self):
        return f"{self.user.username}'s Profile"
