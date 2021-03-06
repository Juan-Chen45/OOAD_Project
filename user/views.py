import os
import sys
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from user.models import ExtendUser
from user.forms import UserModifyForm
from django.urls import reverse
from myfirstsite.views import user_login


# Create your views here.


def user_home(request):
    context = {}
    context['user'] = request.user
    if request.user.is_authenticated:
        context['extendUser'] = ExtendUser.objects.get(user=request.user)
        context['version'] = context['extendUser'].version.all()
        context["dlc"] = context['extendUser'].dlc.all()
        return render(request, 'user_home.html', context)
    else:
        return user_login(request)


def modify_user(request):
    user = request.user
    extend = get_object_or_404(ExtendUser, user=user)
    context = {}
    context.update(csrf(request))
    if request.method == "POST":
        # 当有数据上传时，要把request.FILES传入
        # 同时前端要加enctype="multipart/form-data"

        modify_form = UserModifyForm(request.POST,request.FILES)
        # 验证过了，说明用户验证也成功了
        if modify_form.is_valid():
            user.username = modify_form.cleaned_data["name"]
            extend.introduction =modify_form.cleaned_data["introduction"]
            if(modify_form.cleaned_data['avatar'] is not None):
                extend.avatar = modify_form.cleaned_data['avatar']
            user.save()
            extend.save()
            # redirect 去的地址要改
            return redirect(reverse("user_home"))
    else:
        # 是 get
        initial = {"name": user.username, "introduction": extend.introduction,"avatar":extend.avatar}
        modify_form = UserModifyForm(initial=initial)
    context["user"] = user
    context["extend"] = extend
    context["form"] = modify_form
    return render(request, "modify_user.html", context)
