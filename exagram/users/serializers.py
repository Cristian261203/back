from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)  

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'avatar', 'followers_count', 'following_count']  
