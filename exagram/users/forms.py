from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'email']  # 选择要在表单中显示的字段

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'followers', 'following']