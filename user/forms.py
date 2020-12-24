from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from user.models import ExtendUser


class UserModifyForm(forms.Form):
    name = forms.CharField(label="用户名", max_length=20, min_length=3,
                           widget=forms.TextInput(attrs={"placeholder": "请输入用户名"}))
    introduction = forms.CharField(label="个人简介",empty_value="")
    avatar = forms.ImageField(label="个人头像",required=False)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if User.objects.filter(username=name).exists():
            raise forms.ValidationError("用户名已存在")
        return name
    def clean_introduction(self):
        introduction = self.cleaned_data["introduction"]
        return introduction

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]
        return avatar

