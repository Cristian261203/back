from django.urls import path
from .views import PostListCreateView, LikeCreateView, CommentCreateView

urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/likes/', LikeCreateView.as_view(), name='like-create'),
    path('api/comments/', CommentCreateView.as_view(), name='comment-list-create'),
]
