import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Profile, User  # 只导入自定义的 User 模型
from .serializers import ProfileSerializer
from .forms import UserProfileForm
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return HttpResponse("Hello, welcome to the homepage!")

def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            print(f"Received username: {username}")
            print(f"Received email: {email}")
            print(f"Received password: {password}")

            if not username:
                return JsonResponse({"error": "Username is required"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "User registered successfully"}, status=201)
        except Exception as e:
            print("Error creating user:", e)
            return JsonResponse({"error": f"Failed to create user: {str(e)}"}, status=500)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)  # 使用 Profile 模型实例
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # 更新成功后重定向到个人资料页面
    else:
        form = UserProfileForm(instance=request.user.profile)  # 使用当前用户的 Profile 数据实例化表单
    return render(request, 'users/profile.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def search_users(request):
    query = request.GET.get('query')
    if query:
        users = User.objects.filter(username__icontains=query)
        users_data = [
            {
                "id": user.id,
                "username": user.username,
                "bio": user.profile.bio if hasattr(user, 'profile') else '',
                "avatar": user.avatar.url if user.avatar else None  # 从 User 模型获取 avatar
            } for user in users
        ]
        return JsonResponse(users_data, safe=False)
    else:
        return JsonResponse({"error": "No query provided"}, status=400)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
