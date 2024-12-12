import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import get_token  # 确保导入生成 CSRF Token 的方法
from .models import Profile, User  # 自定义的 User 模型
from .serializers import ProfileSerializer
from .forms import UserProfileForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# 用户注册
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(f"Register request data: {data}")  # 调试打印接收到的数据
            
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # 验证必填字段
            if not username:
                return JsonResponse({"error": "Username is required"}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            # 创建用户
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)  # 注册后自动登录
            
            # 返回成功响应
            return JsonResponse({"message": "User registered successfully"}, status=201)
        except Exception as e:
            print(f"Register error: {str(e)}")  # 打印错误信息
            return JsonResponse({"error": f"Failed to create user: {str(e)}"}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)

@ensure_csrf_cookie  # 确保生成并返回 CSRF Cookie
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 确保返回 CSRF Token
            csrf_token = get_token(request)
            response = JsonResponse({"message": "Login successful"})
            response.set_cookie(
                'csrftoken',  # 注意键名必须为 csrftoken
                csrf_token,
                httponly=False,  # 允许前端访问
                samesite='Lax',
                secure=False  # 开发环境应为 False
            )
            print(f"Set-Cookie Sent: {csrf_token}")  # 调试信息
            return response

        return JsonResponse({"error": "Invalid username or password"}, status=401)

    return JsonResponse({"error": "Invalid method"}, status=405)

# 用户注销
@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"}, status=200)

# 用户资料
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Profile updated successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid data"}, status=400)
    else:
        profile_data = {
            "username": request.user.username,
            "email": request.user.email,
            "bio": request.user.profile.bio if hasattr(request.user, "profile") else "",
            "avatar": request.user.avatar.url if request.user.avatar else None
        }
        return JsonResponse(profile_data, status=200)

# 搜索用户
@login_required
def search_users(request):
    query = request.GET.get('query')
    if query:
        users = User.objects.filter(username__icontains=query)
        users_data = [
            {
                "id": user.id,
                "username": user.username,
                "bio": user.profile.bio if hasattr(user, 'profile') else '',
                "avatar": user.avatar.url if user.avatar else None
            } for user in users
        ]
        return JsonResponse(users_data, safe=False)
    else:
        return JsonResponse({"error": "No query provided"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')  # 确保对整个类禁用 CSRF
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            print(f"Current user: {request.user}")
            if request.user.is_anonymous:
                print("User is anonymous.")

            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=200)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)