from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Like, Comment
from rest_framework import generics
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework_simplejwt.authentication import JWTAuthentication  # 使用 JWT 进行认证
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # 允许任何人读取数据
        if request.method in SAFE_METHODS:
            return True
        # 只有对象的作者才能进行修改
        return obj.author == request.user

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


@method_decorator(csrf_exempt, name='dispatch')
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  
    authentication_classes = []

    def perform_create(self, serializer):
        
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()  

class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
