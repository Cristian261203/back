from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import UserProfileView, search_users
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('profile/', views.profile, name='profile'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),  #
    path('api/search/', search_users, name='search_users'),
]

