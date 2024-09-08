from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm 
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm


def home(request):
    return HttpResponse("Hello, welcome to the homepage!")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)  # 使用实例化的用户更新表单
        if form.is_valid():
            form.save()
            return redirect('profile')  # 更新成功后重定向到个人资料页面
    else:
        form = UserProfileForm(instance=request.user)  # 使用当前用户的数据实例化表单
    return render(request, 'users/profile.html', {'form': form})  # 确保正确传递表单对象