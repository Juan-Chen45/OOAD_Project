from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    # 已经自带必填验证
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"placeholder": "请输入用户名"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

    # 检查用户登录是否有效
    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("用户名或密码错误")
        else:
            self.cleaned_data["user"] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, min_length=3,
                               widget=forms.TextInput(attrs={"placeholder": "请输入用户名"}))
    email = forms.EmailField(label="邮箱", widget=forms.EmailInput(attrs={"placeholder": "请输入邮箱"}))
    password = forms.CharField(label="密码", max_length=20, min_length=3, widget=forms.PasswordInput)
    password_again = forms.CharField(label="再次输入密码", max_length=20, min_length=3, widget=forms.PasswordInput)
    ifDeveloper= forms.BooleanField(required=False)
    # 在clean验证的时候其实可以根据每一个不同的字段进行验证的
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data["password"]
        password_again = self.cleaned_data["password_again"]
        if password != password_again:
            raise forms.ValidationError("密码不一致")
        return password_again

    def clean_ifDeveloper(self):
        ifDeveloper = self.cleaned_data["ifDeveloper"]
        return ifDeveloper