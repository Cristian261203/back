from rest_framework import serializers
from .models import Post, Like, Comment
from users.models import User  

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar']  

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  

    class Meta:
        model = Post
        fields = ['id', 'author', 'image', 'content', 'created_at']
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']
