from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from user.models import ExtendUser


class UserModifyForm(forms.Form):
    curruser = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField(label="用户名", max_length=20, min_length=3)
    introduction = forms.CharField(label="个人简介")
    avatar = forms.ImageField(label="个人头像", required=False)

    def clean_curruser(self):
        curruser = self.cleaned_data["curruser"]
        return curruser

    def clean_name(self):
        name = self.cleaned_data["name"]
        if User.objects.filter(username=name).exists() and name != self.cleaned_data["curruser"]:
            raise forms.ValidationError("用户名已存在")
        return name

    def clean_introduction(self):
        introduction = self.cleaned_data["introduction"]
        return introduction

    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]
        return avatar
