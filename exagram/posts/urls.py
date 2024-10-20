from django.urls import path
from .views import PostListCreateView, LikeCreateView, CommentCreateView, PostUpdateView, PostDeleteView
from django.views.generic import TemplateView

urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/likes/', LikeCreateView.as_view(), name='like-create'),
    path('api/comments/', CommentCreateView.as_view(), name='comment-list-create'),
    path('api/posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('api/posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('test-form/', TemplateView.as_view(template_name='post.html'), name='test-form'),
]

