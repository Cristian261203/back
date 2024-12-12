from django.urls import path
from .views import (
    register,
    user_login,
    logout_view,
    profile,
    UserProfileView,
    search_users,
)

urlpatterns = [
    # 页面路由
    path('register/', register, name='register'),  # 注册
    path('login/', user_login, name='login'),      # 登录
    path('logout/', logout_view, name='logout'),  # 注销
    path('profile/', profile, name='profile'),    # 个人资料

    # API 路由
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),  # REST API 个人资料
    path('api/search/', search_users, name='search_users'),               # 用户搜索
]
