from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Like, Comment
from rest_framework import generics
from .serializers import PostSerializer, LikeSerializer, CommentSerializer


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Like.objects.get_or_create(user=request.user, post=post)
    return redirect('post-detail', pk=pk)

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get('content')
    if content:
        Comment.objects.create(user=request.user, post=post, content=content)
    return redirect('post-detail', pk=pk)

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer