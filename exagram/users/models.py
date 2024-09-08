from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # 用户头像

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 与 User 模型建立一对一关系
    bio = models.TextField(max_length=500, blank=True)  # 用户个人简介
    followers = models.ManyToManyField(User, related_name='profile_followers', blank=True)  # 关注者
    following = models.ManyToManyField(User, related_name='profile_following', blank=True)  # 用户关注的其他人

    def __str__(self):
        return f"{self.user.username}'s Profile"
